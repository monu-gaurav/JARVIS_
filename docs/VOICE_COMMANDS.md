# JARVIS Voice Commands

## Wake and sleep

| Command | Behaviour |
| --- | --- |
| `Hey Jarvis` | Wakes the assistant when the local detector recognizes the phrase. |
| `Stop listening` | Switches to local wake-word-only mode and suppresses spoken output while asleep. |
| `Go to sleep` | Same as `Stop listening`. |
| `Wake up` | Use the wake phrase `Hey Jarvis`; ordinary speech is ignored while asleep. |

Wake-word mode is enabled by default. On first launch, JARVIS remains asleep while the local model is prepared; an Internet connection is required for this one-time setup. While awake, it automatically sleeps after **60 seconds without detected user speech**. If setup fails, it stays silent instead of reverting to always-listening. Use the orb's right-click menu to **WAKE NOW** or retry setup. After saying “Hey Jarvis”, pause briefly before giving the command.

## Change the interface accent color

Examples: 

- `Change JARVIS color to blue`
- `Make the interface purple`
- `Change the orb color to red`
- `Set the theme to green`
- `Use color #ff3355`

Supported names include cyan, teal, ice blue, light blue, blue, navy, red, green, lime, purple, violet, pink, magenta, orange, yellow, gold, white, silver, and turquoise. Hex colors must use the six-digit `#RRGGBB` form. A successful change applies across the interface and is saved to `config/api_keys.json`.

## Listening and wake word

- Say **"Stop listening"** or **"Go to sleep"** to close the microphone-to-AI gate.
- While asleep, the local **"Hey Jarvis"** detector is the only voice path that can wake the assistant. Ordinary speech is not sent to the AI.
- If local wake-word setup fails, JARVIS stays asleep instead of silently reverting to always-listening. Use the orb context menu to choose **WAKE NOW** or retry setup.
- The orb becomes muted blue-grey while asleep and returns to the selected accent colour after waking.
