from cogs.ai_voice import VoiceAssistant
from cogs.spotify import SpotifyManager
from cogs.local_music import LocalMusicPlayer
from data import username, AIname

# Initialize components
voice_assistant = VoiceAssistant(personality="friendly")  # Choose personality: 'friendly', 'sarcastic', 'formal'
spotify_manager = SpotifyManager()
local_music_player = LocalMusicPlayer()

# Voice recognition setup
import speech_recognition as sr

recognizer = sr.Recognizer()

while True:
    try:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            print("Say something...")
            audio = recognizer.listen(source)
            text = recognizer.recognize_google(audio).lower()
            print(f"Input text: {text}")

            # Check for the wake word
            if f"hey {AIname}" in text or f"ok {AIname}" in text:
                voice_assistant.process_command(text)

    except KeyboardInterrupt:
        print("Exiting...")
        break
    except Exception as e:
        print(f"Error: {e}")
        continue
