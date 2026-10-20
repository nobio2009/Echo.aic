import json
import os
import urllib.request
import urllib.error

class HybridAI:
    """Local-first AI with optional online fallback. Uses HTTP stdlib only."""
    def __init__(self, config): self.config = config

    def _post(self, url, payload, headers, timeout):
        req = urllib.request.Request(url, data=json.dumps(payload).encode(), headers={"Content-Type":"application/json", **headers}, method="POST")
        with urllib.request.urlopen(req, timeout=timeout) as response: return json.loads(response.read().decode("utf-8"))

    def _local(self, messages):
        cfg = self.config["local_ai"]
        payload = {"model": cfg["model"], "messages": [{"role":"system","content":"You are Nyx, a concise, helpful desktop voice assistant. Never claim to have performed an action unless a module reports success."}, *messages], "stream": False}
        data = self._post(cfg["base_url"], payload, {}, int(cfg.get("timeout_seconds",45)))
        return data["message"]["content"].strip()

    def _online(self, messages):
        cfg = self.config["online_ai"]
        key = os.environ.get(cfg.get("api_key_env", "NYX_AI_API_KEY"), "")
        if not key: raise RuntimeError(f"API key missing: set environment variable {cfg.get('api_key_env','NYX_AI_API_KEY')}")
        payload = {"model":cfg["model"], "messages":[{"role":"system","content":"You are Nyx, a concise, helpful desktop voice assistant."}, *messages], "temperature":0.5}
        data = self._post(cfg["base_url"], payload, {"Authorization":f"Bearer {key}"}, int(cfg.get("timeout_seconds",45)))
        return data["choices"][0]["message"]["content"].strip()

    def reply(self, history):
        mode = self.config.get("ai_mode", "hybrid").lower()
        errors = []
        if mode in {"hybrid", "local", "ollama"} and self.config["local_ai"].get("enabled", True):
            try: return self._local(history)
            except Exception as exc: errors.append(f"Local AI: {exc}")
        if mode in {"hybrid", "online", "cloud"} and self.config["online_ai"].get("enabled", False):
            try: return self._online(history)
            except Exception as exc: errors.append(f"Online AI: {exc}")
        raise RuntimeError("; ".join(errors) or "No AI backend enabled in config.json")
