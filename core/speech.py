from pathlib import Path
import json, queue, threading, time
from .config import ROOT

class SpeechIO:
    def __init__(self, config, logger=print):
        self.config = config["speech"]
        self.wake_config = config["wake_word"]
        self.log = logger
        self._tts = None
        self._vosk_model = None
        self._audio = None
        self._wake_thread = None
        self._wake_stop = threading.Event()

    def _load_voice(self):
        if self._vosk_model: return True
        try:
            import vosk, sounddevice as sd
            model_path = ROOT / self.config["model_path"]
            if not model_path.exists():
                self.log(f"Offline speech model not found: {model_path}")
                self.log("See README.md for the Vosk model download steps. Typed input and GUI remain available.")
                return False
            vosk.SetLogLevel(-1)
            self._vosk_model = vosk.Model(str(model_path)); self._audio = sd
            return True
        except ImportError as exc:
            self.log(f"Voice dependencies missing ({exc}). Install requirements.txt; typed mode remains available.")
            return False
        except Exception as exc:
            self.log(f"Voice initialisation failed: {exc}"); return False

    def listen_once(self, timeout=None):
        if not self._load_voice(): return None
        import vosk
        rate = int(self.config.get("sample_rate",16000)); device = self.config.get("device_index")
        timeout = int(timeout or self.config.get("max_listen_seconds",12))
        recognizer = vosk.KaldiRecognizer(self._vosk_model, rate)
        chunks = queue.Queue()
        def callback(indata, frames, time_info, status):
            if status: self.log(f"Microphone: {status}")
            chunks.put(bytes(indata))
        start=time.monotonic(); last_audio=start; heard=False
        try:
            with self._audio.RawInputStream(samplerate=rate, blocksize=8000, device=device, dtype="int16", channels=1, callback=callback):
                while time.monotonic()-start < timeout:
                    try: data=chunks.get(timeout=.4)
                    except queue.Empty: continue
                    if recognizer.AcceptWaveform(data):
                        result=json.loads(recognizer.Result()).get("text","").strip()
                        if result: return result
                    partial=json.loads(recognizer.PartialResult()).get("partial","").strip()
                    if partial: heard=True; last_audio=time.monotonic()
                    elif heard and time.monotonic()-last_audio > float(self.config.get("silence_seconds",1.1)):
                        break
                final=json.loads(recognizer.FinalResult()).get("text","").strip()
                return final or None
        except Exception as exc:
            self.log(f"Microphone error: {exc}"); return None

    def speak(self, text):
        if not self.config.get("tts_enabled", True) or not text: return
        try:
            if self._tts is None:
                import pyttsx3
                self._tts=pyttsx3.init(); self._tts.setProperty("rate",int(self.config.get("speech_rate",180)))
            # pyttsx3 can be unhappy if called concurrently from GUI/wake threads.
            self._tts.say(str(text)); self._tts.runAndWait()
        except Exception as exc: self.log(f"Text-to-speech unavailable: {exc}")

    def start_wake_listener(self, callback):
        if not self.wake_config.get("enabled", False) or self._wake_thread and self._wake_thread.is_alive(): return
        self._wake_stop.clear()
        def worker():
            phrase=self.wake_config.get("phrase","hey nyx").lower().strip()
            self.log(f"Wake-word listener active. Say '{phrase}'.")
            while not self._wake_stop.is_set():
                heard=self.listen_once(timeout=4)
                if heard and phrase in heard.lower():
                    self.log("Wake word detected.")
                    callback()
            self.log("Wake-word listener stopped.")
        self._wake_thread=threading.Thread(target=worker,daemon=True,name="nyx-wake-listener"); self._wake_thread.start()

    def stop_wake_listener(self): self._wake_stop.set()
