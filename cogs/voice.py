import pyttsx3
from datetime import datetime
from cogs.local_music import LocalMusicPlayer
from cogs.spotify import SpotifyManager

class VoiceAssistant:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.engine.setProperty('voice', self.engine.getProperty('voices')[0].id)

    def say(self, message):
        self.engine.say(message)
        self.engine.runAndWait()

    def process_command(self, recognizer, source):
        #variables
        local_music_player = LocalMusicPlayer()
        spotify_manager = SpotifyManager()

        # Ask for input after the wake word
        self.say("What can I do for you?")
        try:
            # Listen for the user's command
            audio = recognizer.listen(source)
            command = recognizer.recognize_google(audio).lower()
            print(f"Command received: {command}")

            # Handle recognized commands
            # Miscellaneous commands
            if "say hello" in command:
                self.say("Hello, how can I assist you?")
            elif "what time is it" in command:
                current_time = datetime.now().strftime("%H:%M")
                self.say(f"The time is {current_time}")

            # Local music commands
            elif "play music" in command:
                local_music_player.play()
            
            elif "pause music" in command:
                local_music_player.pause()
            
            elif "skip music" in command:
                local_music_player.skip()
            
            # Spotify commands
            elif "play spotify" in command:
                spotify_manager.play()
            
            elif "pause spotify" in command:
                spotify_manager.pause()

            elif "next track" in command:
                spotify_manager.next_track()

            elif "go back a song" in command:
                spotify_manager.previous_track()

            elif "what song is this" in command:
                current_song = spotify_manager.get_current_song()
                self.say(f"The current song is {current_song}")

            # Exit command
            elif "exit" in command:
                self.say("Goodbye!")
                return "exit"
            else:
                self.say("I didn't understand that command.")
        except Exception as e:
            print(f"Error recognizing command: {e}")
            self.say("I couldn't catch that. Please try again.")

        # Return None if no "exit" command is detected
        return None
