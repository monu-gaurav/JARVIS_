# JARVIS — Quick Start

**Owner / Maintainer:** Monu Gaurav · [GitHub](https://github.com/monu-gaurav) · [LinkedIn](https://www.linkedin.com/in/monu-gaurav-0b3329330/)

This version starts with **only a small animated JARVIS reactor orb** in the bottom-right corner. The regular CPU/RAM/temperature dashboard is not shown during normal use. The assistant engine and its existing skills are retained.

## Windows setup

1. Extract the entire `JARVIS` folder from the ZIP to a normal folder, for example `Documents\JARVIS`. Do not run it from inside the ZIP.
2. Install **Python 3.12 (64-bit)** if it is not already installed. During installation, enable the Python Launcher and add Python to PATH.
3. Double-click `INSTALL_JARVIS.bat` and let it finish.
4. Double-click `START_JARVIS.bat`. On the first launch, a small setup window asks for your Gemini API key and computer type.
5. After saving the key, the setup window closes and the animated orb appears in the bottom-right corner.

Use `DEBUG_JARVIS.bat` if startup fails; it keeps the terminal visible so you can read the error.

## Using the orb

- **Drag with the left mouse button** to move the orb to another corner.
- **Right-click the orb** for microphone mute/unmute, wake/sleep (when wake-word mode is enabled), phone pairing, API setup, or exit.
- Wake-word mode is on by default. On first use, JARVIS stays asleep while it prepares the local model. Say **“Hey Jarvis”**, pause briefly, then speak your command. It automatically sleeps after 60 seconds without detected user speech. Say **“Stop listening”** to sleep immediately. If setup fails, it stays silent; right-click the orb and choose **WAKE NOW** or retry setup.
- The orb changes its glow while JARVIS is listening, thinking, or speaking. It does not show CPU usage, memory usage, temperatures, logs, or other telemetry. Continuous hardware monitoring is disabled; JARVIS can still answer a direct system-status question when requested.

## Use JARVIS from an Android phone

1. Start JARVIS on the Windows PC.
2. Make sure the phone and PC are on the same Wi-Fi network.
3. Right-click the orb and choose **Connect phone…**.
4. Scan the QR code with your phone camera and open the companion page. Pairing codes are temporary.

This project provides a **phone-browser companion**, not a separately compiled Android APK. The phone companion starts only after you request phone pairing; it is not exposed on the network just because the orb is launched. Windows may ask permission for local-network access when you first enable phone pairing.

## Start JARVIS when you sign in to Windows

Double-click `ENABLE_WINDOWS_STARTUP.bat` once to create a shortcut in your Windows Startup folder. Run `DISABLE_WINDOWS_STARTUP.bat` to remove it.

## API key and privacy notes

- No API key is included in this package. Create or manage a Gemini API key at [Google AI Studio](https://aistudio.google.com/app/apikey).
- The key is stored locally in `config\api_keys.json`; do not share that file or upload it publicly. This distributable source archive intentionally excludes API-key and personal-memory files.
- This assistant needs Internet access for its Gemini voice/AI session. Free usage quotas and model availability depend on the API provider and may change. “Free tools” does not mean unlimited hosted AI usage.
- Camera vision is optional and should be invoked deliberately. Smart-home control requires compatible devices/services and their own setup.
- Desktop automation actions can affect files and applications. Review commands before using them for important or destructive tasks.

## Troubleshooting

- If the orb does not appear, open `DEBUG_JARVIS.bat` and read the displayed error.
- If speech does not work, verify Windows microphone/speaker permissions and the selected default audio device.
- If the AI connection is rejected, right-click the orb → **API key / setup…** and enter a valid key.
- For phone pairing, confirm both devices are on the same network and allow JARVIS through Windows Firewall for a private network if prompted.
