# Nyx Assistant 2.0

A modular Python desktop voice assistant with a Tkinter GUI, offline speech recognition (Vosk), optional speech synthesis, a local-first hybrid AI client (Ollama + optional OpenAI-compatible API), plugin modules, lightweight local conversation history, wake-word listening, and configurable homelab service checks.

## Requirements
- Python 3.10+
- Windows, Linux, or macOS
- Optional voice input: `vosk` + `sounddevice` and a downloaded Vosk model
- Optional voice output: `pyttsx3`
- Optional CPU/RAM metrics: `psutil`
- Optional local AI: Ollama with a model downloaded
- Optional online AI: API key in an environment variable

## Install (Windows PowerShell)
```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```
If PowerShell blocks activation, use CMD with `.venv\Scripts\activate.bat`, or run `.venv\Scripts\python.exe main.py` directly.

## Enable offline speech recognition
Download a Vosk English model from https://alphacephei.com/vosk/models. The small US English model is named `vosk-model-small-en-us-0.15`. Extract it so the directory is exactly:

`models/vosk-model-small-en-us-0.15/`

The directory should contain model files such as `am`, `conf`, `graph` and `ivector` (the exact contents vary by model). The model is not bundled in this ZIP because it is large and separately licensed. Configure `speech.model_path` in `config.json` for another model/language. Recognition itself runs locally and does not send audio to a cloud service.

Install sound-device support if needed and check your microphone privacy permissions. Set `speech.device_index` to a sounddevice device index if the default microphone is wrong.

## Start
```powershell
python main.py
```
The Tkinter desktop GUI includes a text field, a Listen button, and an optional wake-word toggle. The app still starts without voice dependencies/model; typed commands remain available.

### Wake word notes
Enable the checkbox in the GUI and say the configured phrase (default `hey nyx`). Wake detection is offline and uses the Vosk speech model. It is software keyword detection, not a dedicated low-power wake-word engine; the microphone remains active while enabled. Disable it in the GUI when not needed. Some systems allow only one microphone stream at a time, so the wake listener and manual Listen button may conflict on certain audio drivers.

## Configure AI
Default `ai_mode` is `hybrid`. It tries the local Ollama backend first; if that fails, it tries the online backend only if `online_ai.enabled` is `true` and the API key environment variable is set.

### Local AI (recommended default)
Install Ollama from https://ollama.com/, then:
```powershell
ollama pull llama3.2
```
Leave `local_ai.enabled` set to `true`. Ollama usually listens on `http://127.0.0.1:11434`.

### Optional online fallback
Set `online_ai.enabled` to `true` in `config.json`. Set your key as an environment variable; for example, in PowerShell:
```powershell
$env:NYX_AI_API_KEY = "your-key-here"
```
Use a provider endpoint compatible with the OpenAI Chat Completions API, and configure `online_ai.base_url` and `online_ai.model`. The app never writes your API key into config or logs it. Online prompts/history are sent to that provider when its fallback is used; do not put secrets in conversation history.

To disable AI, set `ai_mode` to `off`. The modules still work.

## Homelab integration
Edit `homelab.services` in `config.json`:
```json
"homelab": {
  "services": [
    {"name":"jellyfin", "url":"http://192.168.1.20:8096", "timeout_seconds":4},
    {"name":"grafana", "url":"http://192.168.1.20:3000", "health_url":"http://192.168.1.20:3000/api/health", "timeout_seconds":4}
  ]
}
```
Use your actual LAN addresses and ports. Commands: `run services` and `run service jellyfin`. These are simple HTTP reachability checks; they do not authenticate or administer services. Prefer Tailscale/private LAN addresses and do not expose services to the public internet just for this assistant.

## Commands
- `help`
- `run time`
- `run status`
- `run services`
- `run service jellyfin`
- `run openurl https://example.com`
- `ask Explain recursion`
- `exit`

## Add a module
Create `modules/example_module.py`:
```python
def register(assistant):
    def hello(argument=""):
        return f"Hello {argument or 'there'}!"
    assistant.command("hello", "Say hello.", hello)
```
Restart Nyx. Modules are trusted Python code and run with the same permissions as the user. Only install modules you trust. Nyx intentionally does not expose arbitrary shell execution. Add privileged actions only with explicit allowlists and confirmation.

## Project layout
```text
main.py
config.json
core/
  app.py          # Tkinter GUI + startup
  assistant.py    # command router, plugin loader, local history
  ai.py           # local-first hybrid AI client
  speech.py       # Vosk offline speech, TTS, wake phrase
  config.py        # configuration defaults and paths
modules/
  homelab_module.py
  open_url_module.py
  system_module.py
  time_module.py
data/              # history generated at runtime
models/            # place Vosk model here (not included)
```

## Troubleshooting
- **GUI won't open:** verify Tkinter is included with your Python install; console fallback is provided.
- **No voice model:** extract a Vosk model at the configured path; use typed input in the meantime.
- **Microphone unavailable:** check OS permissions and `sounddevice.query_devices()` from Python.
- **Ollama error:** start Ollama and verify `ollama list` includes the configured model.
- **Online fallback not used:** set `ai_mode` to `hybrid`, enable `online_ai.enabled`, and define the configured API-key environment variable.
