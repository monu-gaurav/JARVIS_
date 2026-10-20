# JARVIS — Personal AI Assistant

JARVIS is a voice-controlled desktop assistant with a compact animated reactor orb, computer automation, file tools, web search, memory, a phone-browser companion, and a locally detected **“Hey Jarvis”** wake phrase.

## Owner and links

| **Owner / Maintainer** | Monu Gaurav |
| **GitHub** | [github.com/monu-gaurav](https://github.com/monu-gaurav) |
| **LinkedIn** | [linkedin.com/in/monu-gaurav-0b3329330](https://www.linkedin.com/in/monu-gaurav-0b3329330/) |

## Features

- **Voice conversation** with a Gemini Live model and configurable voice.
- **Wake-word privacy gate:** local “Hey Jarvis” detection keeps microphone audio off the AI connection while asleep.
- **Automatic idle sleep:** after **60 seconds without user speech**, JARVIS sleeps and waits for “Hey Jarvis”.
- **Voice-controlled sleep:** say **“stop listening”** or **“go to sleep”** to enter sleep mode immediately. JARVIS stays silent until the local detector hears “Hey Jarvis”.
- **Voice-controlled interface color:** ask for colors such as blue, red, green, purple, pink, orange, yellow, cyan, or say a custom `#RRGGBB` value. The selection is applied and saved.
- **Computer and file tools:** open apps, handle files, browse the web, inspect the screen on request, and use other discovered actions.
- **Long-term memory** stored locally, an undo system for supported changes, reminders, and pluggable actions.
- **Compact animated orb** and a phone-browser companion for remote interaction on the same network.
- **Customizable assistant identity, voice, and accent color** from the settings/customization UI.

## Voice commands

| Say | Result |
| --- | --- |
| “Hey Jarvis” | Wake JARVIS from sleep using local wake-word detection. |
| “Stop listening” | Stop cloud-bound microphone audio and sleep until “Hey Jarvis” is detected. |
| “Go to sleep” | Same as “stop listening”. |
| “Change JARVIS color to blue” | Change the interface accent color and save it. |
| “Make the interface purple” | Apply a different accent color. |
| “Use color `#ff3355`” | Apply a custom six-digit hex color. |

The local wake-word engine and model are installed on demand the first time sleep mode is needed. On first setup, keep Internet access available until the installation finishes. The desktop settings also include a **WAKE WORD** control if you prefer to set it up before using voice sleep commands.

## Install on Windows

### Requirements

- Windows 10 or Windows 11
- Python **3.12, 64-bit**, with the Python Launcher enabled and Python added to `PATH`
- A microphone and speakers/headphones
- A Gemini API key from [Google AI Studio](https://aistudio.google.com/app/apikey)
- Internet access for Gemini Live, web features, and first-time wake-word installation

### Steps

1. Download or clone this repository, then extract it into a normal folder such as `Documents\JARVIS`. Do not run it from inside an archive.
2. Double-click `INSTALL_JARVIS.bat` and let the dependency installation finish.
3. Double-click `START_JARVIS.bat`.
4. On the first launch, paste your Gemini API key into the setup dialog and select your operating system.
5. When the orb appears, say a command. The wake-word detector is prepared on demand; after setup, JARVIS sleeps after 60 seconds of inactivity.

If startup fails, run `DEBUG_JARVIS.bat` to keep the terminal visible and inspect the error message.

### Manual setup

```powershell
py -3.12 -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m playwright install chromium firefox
python main.py
```

## Project structure

```text
JARVIS/
├── actions/                  # Built-in tools and computer-control actions
├── config/                   # Runtime configuration and app icon (secrets are not committed)
├── core/                     # Wake-word detection, speech, plugins, installer, undo, prompts
├── dashboard/                # Phone-browser companion and static web UI
├── docs/                     # Project structure and voice-command reference
├── memory/                   # Local memory and configuration helpers
├── plugins/                  # Extensible plugin examples and plugins
├── .gitignore
├── DEBUG_JARVIS.bat
├── DISABLE_WINDOWS_STARTUP.bat
├── ENABLE_WINDOWS_STARTUP.bat
├── INSTALL_JARVIS.bat
├── LICENSE
├── README.md
├── START_HERE.md
├── START_JARVIS.bat
├── main.py                   # Voice session, tool routing, and sleep/wake state
├── requirements.txt
├── setup.py
└── ui.py                     # Desktop window, orb, theme, and settings UI

