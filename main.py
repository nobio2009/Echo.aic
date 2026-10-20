import speech_recognition as sr
from cogs.voice import VoiceAssistant
from cogs.spotify import SpotifyManager
from cogs.local_music import LocalMusicPlayer
from data import username, AIname

# Initialize components
voice_assistant = VoiceAssistant()
spotify_manager = SpotifyManager()
local_music_player = LocalMusicPlayer()

# Voice recognition setup
recognizer = sr.Recognizer()

while True:
    try:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            print('Say something...')
            audio = recognizer.listen(source)
            text = recognizer.recognize_google(audio).lower()
            print(f"Input text: {text}")

            # Check if wake word is present
            if f'hey {AIname}' in text or f'ok {AIname}' in text:
                # Delegate command processing
                response = voice_assistant.process_command(recognizer, source)

                if response == "exit":
                    break

    except KeyboardInterrupt:
        break
    except Exception as e:
        print(f"Error: {e}")
        continue

print("Goodbye!")
