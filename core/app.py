import threading
import tkinter as tk
from tkinter import ttk, messagebox
from .config import load_config
from .ai import HybridAI
from .speech import SpeechIO
from .assistant import Assistant

class NyxGUI:
    def __init__(self, config, assistant, speech):
        self.config,self.assistant,self.speech=config,assistant,speech
        gui=config["gui"]; self.root=tk.Tk(); self.root.title(gui.get("title","Nyx Assistant")); self.root.geometry(f"{gui.get('width',900)}x{gui.get('height',650)}")
        self.root.protocol("WM_DELETE_WINDOW",self.close)
        outer=ttk.Frame(self.root,padding=12); outer.pack(fill="both",expand=True)
        ttk.Label(outer,text=f"{config['assistant_name']} Assistant",font=("Segoe UI",18,"bold")).pack(anchor="w")
        ttk.Label(outer,text="Local-first AI · Offline speech · Modular tools").pack(anchor="w",pady=(0,10))
        self.output=tk.Text(outer,wrap="word",state="disabled",height=20); self.output.pack(fill="both",expand=True)
        row=ttk.Frame(outer); row.pack(fill="x",pady=(10,0))
        self.entry=ttk.Entry(row); self.entry.pack(side="left",fill="x",expand=True); self.entry.bind("<Return>",lambda _e:self.send_text())
        ttk.Button(row,text="Send",command=self.send_text).pack(side="left",padx=(6,0))
        ttk.Button(row,text="🎙 Listen",command=self.listen).pack(side="left",padx=(6,0))
        self.wake_var=tk.BooleanVar(value=False)
        ttk.Checkbutton(outer,text=f"Enable wake word ({config['wake_word'].get('phrase','hey nyx')})",variable=self.wake_var,command=self.toggle_wake).pack(anchor="w",pady=(8,0))
        self.append("Nyx", "Ready. Type 'help' for commands. Offline speech requires the Vosk model; AI requires Ollama or configured online credentials.")

    def append(self, who, text):
        self.output.configure(state="normal"); self.output.insert("end",f"{who}: {text}\n\n"); self.output.see("end"); self.output.configure(state="disabled")

    def _process(self, text):
        if not text: self.append("Nyx","No speech detected. Try again or type a command."); return
        self.append("You",text)
        def worker():
            answer=self.assistant.handle(text)
            self.root.after(0,lambda:self.append("Nyx",answer))
            self.speech.speak(answer)
        threading.Thread(target=worker,daemon=True).start()

    def send_text(self):
        text=self.entry.get().strip(); self.entry.delete(0,"end"); self._process(text)

    def listen(self):
        self.append("Nyx","Listening…")
        def worker():
            text=self.speech.listen_once()
            self.root.after(0,lambda:self._process(text))
        threading.Thread(target=worker,daemon=True).start()

    def toggle_wake(self):
        if self.wake_var.get():
            self.speech.start_wake_listener(lambda:self.root.after(0,self._wake_command))
        else: self.speech.stop_wake_listener()

    def _wake_command(self):
        self.append("Nyx","Wake word detected. Listening for a command…")
        def worker():
            text=self.speech.listen_once(timeout=int(self.config["wake_word"].get("command_timeout_seconds",10)))
            self.root.after(0,lambda:self._process(text))
        threading.Thread(target=worker,daemon=True).start()

    def close(self):
        self.speech.stop_wake_listener(); self.root.destroy()

    def run(self): self.root.mainloop()

def main():
    config=load_config()
    # Tkinter is the default UI; if it cannot initialise, offer a console fallback.
    app_ref={}
    def log(message):
        gui=app_ref.get("gui")
        if gui: gui.root.after(0,lambda:gui.append("System",message))
        else: print(message)
    ai=HybridAI(config) if config.get("ai_mode")!="off" else None
    speech=SpeechIO(config,log)
    assistant=Assistant(config,ai,speech,log)
    try:
        gui=NyxGUI(config,assistant,speech); app_ref["gui"]=gui; gui.run()
    except tk.TclError as exc:
        print(f"GUI unavailable ({exc}); using console mode. Type 'exit' to quit.")
        while True:
            try: text=input("You> ")
            except (EOFError,KeyboardInterrupt): break
            answer=assistant.handle(text); print(f"Nyx> {answer}")
            if text.strip().lower() in {"exit","quit","goodbye"}: break
