# Project Structure

The top-level packages are kept stable so imports and existing actions continue to work. Documentation and owner metadata are grouped separately.

| Path | Purpose |
| --- | --- |
| `main.py` | Gemini Live session, audio flow, tool declarations/dispatch, wake and sleep state machine. |
| `ui.py` | PyQt desktop host, animated orb, settings/customization panels, theme colors, and thread-safe UI signals. |
| `actions/` | Built-in action modules discovered automatically at launch. |
| `core/` | Speech, local wake-word engine, plugin/action loaders, confirmations, undo, installer, and system prompt. |
| `memory/` | Memory persistence and configuration helpers; local memory data is not bundled. |
| `plugins/` | Optional plugin modules and the plugin template. |
| `dashboard/` | Companion web server plus the phone-browser frontend. |
| `config/` | App icon and runtime configuration; `api_keys.json` is user-created and must stay private. |
| `docs/` | Voice-command and structure references. |
| `tests/` | Regression tests for wake-word score filtering and legacy config migration. |
| `README.md` | Project overview, setup, owner profile, safety, and licensing notes. |
| `OWNER.md` | Owner and maintainer contact links. |
| `NOTICE.md` | Upstream attribution and derivative-work details. |
| `LICENSE` | CC BY-NC 4.0 legal text and attribution header. |
| `requirements.txt` | Python runtime and optional integration dependencies. |
| `setup.py` | Cross-platform dependency setup helper. |
| `*_JARVIS.bat` / startup `.bat` files | Windows install, launch, debugging, and startup controls. |

## Local-only files

Do not commit `config/api_keys.json`, `.env`, certificates, OAuth tokens, linked messaging sessions, or personal memory files. The repository `.gitignore` excludes these paths. A distributable source archive should omit runtime caches such as `__pycache__/` and `*.pyc` as well.
