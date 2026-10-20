from pathlib import Path
import json

ROOT = Path(__file__).resolve().parent.parent
DEFAULTS = {
    "assistant_name": "Nyx", "ai_mode": "hybrid",
    "local_ai": {"enabled": True, "provider": "ollama", "base_url": "http://127.0.0.1:11434/api/chat", "model": "llama3.2", "timeout_seconds": 45},
    "online_ai": {"enabled": False, "provider": "openai_compatible", "base_url": "https://api.openai.com/v1/chat/completions", "model": "gpt-4o-mini", "api_key_env": "NYX_AI_API_KEY", "timeout_seconds": 45},
    "speech": {"enabled": True, "sample_rate": 16000, "model_path": "models/vosk-model-small-en-us-0.15", "device_index": None, "silence_seconds": 1.1, "max_listen_seconds": 12, "tts_enabled": True, "speech_rate": 180},
    "wake_word": {"enabled": True, "phrase": "hey nyx", "command_timeout_seconds": 10},
    "homelab": {"services": []}, "memory": {"enabled": True, "history_file": "data/history.json", "max_messages": 12},
    "gui": {"title": "Nyx Assistant", "width": 900, "height": 650}
}

def _merge(base, incoming):
    result = dict(base)
    for key, value in incoming.items():
        if isinstance(value, dict) and isinstance(result.get(key), dict): result[key] = _merge(result[key], value)
        else: result[key] = value
    return result

def load_config():
    path = ROOT / "config.json"
    if not path.exists(): path.write_text(json.dumps(DEFAULTS, indent=2), encoding="utf-8")
    try: supplied = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc: raise RuntimeError(f"Could not read config.json: {exc}") from exc
    return _merge(DEFAULTS, supplied)
