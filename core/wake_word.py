"""
Local wake-word detection for JARVIS ("Hey Jarvis").

Design goals:
  • ZERO cost when the feature is off — openwakeword is imported ONLY inside
    start()/install helpers, never at module load. If the user never enables
    wake word, none of this touches the app.
  • ZERO latency on the audio path — the microphone callback only ever does a
    cheap, non-blocking queue push (feed()); the actual model inference runs in
    this module's own background thread, so the real-time audio thread and the
    Gemini stream are never slowed.
  • Fully local & offline — audio fed here never leaves the machine; there is no
    network call except the one-time model download the user triggers from the UI.

openwakeword ships small ONNX models (a few MB each) and runs comfortably on a
CPU. The pretrained wake phrase used here is "Hey Jarvis".
"""
from __future__ import annotations

import queue
import subprocess
import sys
import threading
from pathlib import Path
from typing import Callable

# Pretrained openwakeword model that listens for "Hey Jarvis".
WAKE_MODEL = "hey_jarvis"
# Score in [0,1]; above this counts as a detection. Tunable per environment.
DEFAULT_THRESHOLD = 0.62
REQUIRED_CONSECUTIVE_HITS = 2
LOW_SCORE_RESET_THRESHOLD = 0.20
# Mic frames arrive at 16 kHz int16; this is just the detector's input rate.
SAMPLE_RATE = 16000


def is_installed() -> bool:
    """True if the openwakeword package is importable (no model check)."""
    try:
        import importlib.util
        return importlib.util.find_spec("openwakeword") is not None
    except Exception:
        return False


def is_ready() -> bool:
    """True if openwakeword is installed AND its model files are present on disk.

    This is a cheap, DETERMINISTIC file-existence check. It deliberately does NOT
    construct a Model to probe readiness — doing that is slow and, worse, can clash
    with the detector's own Model when it's already running, which intermittently
    returned False and made the UI flicker to 'not downloaded'. Never raises.
    """
    if not is_installed():
        return False
    try:
        import openwakeword
        models_dir = Path(openwakeword.__file__).resolve().parent / "resources" / "models"
        if not models_dir.is_dir():
            return False
        has_wake = (any(models_dir.glob(f"{WAKE_MODEL}*.onnx"))
                    or any(models_dir.glob(f"{WAKE_MODEL}*.tflite")))
        has_mel = (any(models_dir.glob("melspectrogram*.onnx"))
                   or any(models_dir.glob("melspectrogram*.tflite")))
        has_emb = (any(models_dir.glob("embedding_model*.onnx"))
                   or any(models_dir.glob("embedding_model*.tflite")))
        return bool(has_wake and has_mel and has_emb)
    except Exception:
        return False


def install_and_download(logger: Callable[[str], None] = print) -> tuple[bool, str]:
    """
    One-click setup for the UI button: pip-install openwakeword if missing, then
    download the wake model. Returns (ok, message). Never raises — every failure
    is reported through the returned message and the logger.
    """
    try:
        if not is_installed():
            logger("Wake word: installing openwakeword (one-time)…")
            r = subprocess.run(
                [sys.executable, "-m", "pip", "install", "openwakeword"],
                capture_output=True, text=True,
            )
            if r.returncode != 0:
                tail = (r.stderr or r.stdout or "").strip().splitlines()[-1:] or [""]
                return False, f"pip install failed: {tail[0][:160]}"
        # Download the pretrained melspectrogram/embedding + wake models.
        logger("Wake word: downloading models…")
        try:
            import openwakeword.utils as _u
            try:
                _u.download_models([WAKE_MODEL])
            except TypeError:
                _u.download_models()   # older signature downloads the default set
        except Exception as e:
            return False, f"model download failed: {e}"

        if not is_ready():
            return False, "installed, but the wake model could not be loaded."
        logger("Wake word: ready.")
        return True, "Wake word installed and ready."
    except Exception as e:
        return False, f"setup error: {e}"


def _jarvis_model_score(scores) -> float:
    """Return the best score for a JARVIS model only; unrelated models never wake it."""
    if not isinstance(scores, dict):
        return 0.0
    matched = []
    for key, value in scores.items():
        if "jarvis" not in str(key).lower():
            continue
        try:
            matched.append(float(value))
        except (TypeError, ValueError):
            continue
    return max(matched, default=0.0)


class WakeWordDetector:
    """
    Runs the wake model in a dedicated thread. The mic thread calls feed() with
    raw int16 frames; detections invoke on_detect() (called from this thread —
    the callback must marshal to whatever loop/UI it needs).
    """

    def __init__(self, on_detect: Callable[[int], None],
                 threshold: float = DEFAULT_THRESHOLD,
                 logger: Callable[[str], None] = print):
        self._on_detect = on_detect
        self._threshold = threshold
        self._logger    = logger
        self._queue: queue.Queue = queue.Queue(maxsize=50)
        self._thread: threading.Thread | None = None
        self._running = False
        self._model = None
        self._ready = False
        self._consecutive_hits = 0
        self._latched = False
        self._generation = 0
        self._score_lock = threading.Lock()

    def start(self) -> bool:
        """Load the model and spawn the inference thread. Returns True on success.
        Safe to call again — a no-op if already running. Never raises."""
        if self._running:
            return True
        try:
            from openwakeword.model import Model
            self._model = Model(wakeword_models=[WAKE_MODEL], inference_framework="onnx")
        except Exception as e:
            self._logger(f"Wake word: could not load model — {e}")
            self._model = None
            return False
        self._running = True
        self._ready = True
        self._thread = threading.Thread(target=self._loop, daemon=True, name="WakeWordThread")
        self._thread.start()
        self._logger("Wake word: listening for 'Hey Jarvis'.")
        return True

    def stop(self) -> None:
        self._running = False
        # unblock the thread if it's waiting on the queue
        try:
            self._queue.put_nowait(None)
        except Exception:
            pass
        with self._score_lock:
            self._generation += 1
            self._consecutive_hits = 0
            self._latched = False
        self._model = None
        self._ready = False

    def reset(self) -> None:
        """Forget previous detections and discard stale audio between sleep cycles."""
        with self._score_lock:
            self._generation += 1
            self._consecutive_hits = 0
            self._latched = False
        self._drain()

    @property
    def ready(self) -> bool:
        return self._ready

    @property
    def generation(self) -> int:
        """Current sleep-cycle token; stale inference results are ignored."""
        with self._score_lock:
            return self._generation

    def feed(self, frame_int16) -> None:
        """Called from the mic callback (real-time thread). Must stay cheap and
        never block — the frame is copied and dropped if the queue is backed up."""
        if not self._running:
            return
        try:
            # frame_int16 is a numpy int16 array (possibly 2-D mono) — flatten to 1-D
            data = frame_int16[:, 0].copy() if getattr(frame_int16, "ndim", 1) > 1 else frame_int16.copy()
            with self._score_lock:
                generation = self._generation
            self._queue.put_nowait((generation, data))
        except queue.Full:
            pass
        except Exception:
            pass

    def _loop(self) -> None:
        import numpy as np
        while self._running:
            try:
                item = self._queue.get()
                if item is None or not self._running:
                    break
                frame_generation, frame = item
                scores = self._model.predict(np.asarray(frame, dtype=np.int16))
                # Only the actual JARVIS wake model may wake the assistant. Never
                # fall back to the maximum score from an unrelated model.
                score = _jarvis_model_score(scores)
                with self._score_lock:
                    # reset() invalidates any prediction that started before the
                    # current sleep cycle, even if inference completed late.
                    if frame_generation != self._generation:
                        continue
                    should_detect = False
                    if score <= LOW_SCORE_RESET_THRESHOLD:
                        self._consecutive_hits = 0
                        self._latched = False
                    elif not self._latched and score >= self._threshold:
                        self._consecutive_hits += 1
                        if self._consecutive_hits >= REQUIRED_CONSECUTIVE_HITS:
                            self._latched = True
                            self._consecutive_hits = 0
                            should_detect = True
                    elif not self._latched:
                        self._consecutive_hits = 0
                if should_detect:
                    # Keep the real-time microphone callback unblocked: dispatch the
                    # callback outside the score lock, carrying the cycle generation.
                    self._drain()
                    with self._score_lock:
                        if frame_generation != self._generation:
                            continue
                    try:
                        self._logger(f"Wake word detected (confidence {score:.2f}).")
                        self._on_detect(frame_generation)
                    except Exception as e:
                        self._logger(f"Wake word: on_detect error — {e}")
            except Exception as e:
                self._logger(f"Wake word: inference error — {e}")

    def _drain(self) -> None:
        try:
            while True:
                self._queue.get_nowait()
        except Exception:
            pass
