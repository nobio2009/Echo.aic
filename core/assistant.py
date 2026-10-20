from pathlib import Path
import importlib.util
import json
import re
from .config import ROOT

class Assistant:
    def __init__(self, config, ai, speech, logger=print):
        self.config, self.ai, self.speech, self.log = config, ai, speech, logger
        self.commands = {}
        self.history_path = ROOT / config["memory"].get("history_file", "data/history.json")
        self.history = self._load_history()
        self._load_modules()

    def _load_history(self):
        if not self.config["memory"].get("enabled", True): return []
        try:
            data = json.loads(self.history_path.read_text(encoding="utf-8"))
            return data if isinstance(data, list) else []
        except (OSError, json.JSONDecodeError): return []

    def _save_history(self):
        if not self.config["memory"].get("enabled", True): return
        self.history_path.parent.mkdir(parents=True, exist_ok=True)
        limit = max(2, int(self.config["memory"].get("max_messages", 12)))
        self.history = self.history[-limit:]
        self.history_path.write_text(json.dumps(self.history, indent=2), encoding="utf-8")

    def command(self, name, description, callback):
        self.commands[name.lower()] = (description, callback)

    def _load_modules(self):
        folder = ROOT / "modules"
        for path in sorted(folder.glob("*_module.py")):
            try:
                spec = importlib.util.spec_from_file_location(f"nyx_plugin_{path.stem}", path)
                module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
                module.register(self)
                self.log(f"Loaded module: {path.stem}")
            except Exception as exc: self.log(f"Module {path.name} failed to load: {exc}")

    def help_text(self):
        lines = ["Commands: help, ask <question>, status, services, service <name>, open <url>, exit"]
        lines.extend(f"  {name}: {desc}" for name, (desc, _) in sorted(self.commands.items()))
        return "\n".join(lines)

    def handle(self, text):
        text = text.strip()
        if not text: return "I didn't catch that. Please try again."
        self.log(f"You: {text}")
        low = text.lower()
        if low in {"exit", "quit", "goodbye", "shut down assistant"}: return "Goodbye."
        if low in {"help", "what can you do", "commands"}: return self.help_text()
        if low in {"status", "system status", "computer status"} and "status" in self.commands:
            return self.commands["status"][1]("")
        match = re.match(r"^(?:run|do)\s+([\w-]+)(?:\s+(.*))?$", text, re.I)
        if match and match.group(1).lower() in self.commands:
            name, arg = match.group(1).lower(), match.group(2) or ""
            try: return str(self.commands[name][1](arg))
            except Exception as exc: return f"That module failed: {exc}"
        if low.startswith("ask "): text = text[4:].strip()
        elif low.startswith("hey nyx "): text = text[8:].strip()
        # Let modules handle natural-language aliases before calling AI.
        for name, (_, callback) in self.commands.items():
            if name in low:
                try:
                    result = callback(text)
                    if result: return str(result)
                except Exception: pass
        if self.ai:
            try:
                self.history.append({"role": "user", "content": text})
                answer = self.ai.reply(self.history)
                self.history.append({"role": "assistant", "content": answer})
                self._save_history()
                return answer
            except Exception as exc:
                self.log(f"AI unavailable: {exc}")
                return f"I couldn't reach an AI backend. Local commands still work. Details: {exc}"
        return "I don't have a module for that yet. Type 'help' to see available commands."
