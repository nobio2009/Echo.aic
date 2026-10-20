import os

import spotipy
from spotipy.oauth2 import SpotifyOAuth


class SpotifyManager:
    def __init__(self):
        self.client_id = os.getenv("SPOTIFY_CLIENT_ID")
        self.client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
        if not self.client_id or not self.client_secret:
            raise RuntimeError(
                "Set SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET before using Spotify."
            )

        self.redirect_uri = os.getenv(
            "SPOTIFY_REDIRECT_URI", "http://localhost:2009/"
        )
        self.scope = "user-read-playback-state, user-modify-playback-state"

        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=self.client_id,
            client_secret=self.client_secret,
            redirect_uri=self.redirect_uri,
            scope=self.scope
        ))

    def play(self):
        self.sp.start_playback()

    def pause(self):
        self.sp.pause_playback()

    def next_track(self):
        self.sp.next_track()

    def previous_track(self):
        self.sp.previous_track()

    def get_current_song(self):
        music_data = self.sp.current_user_playing_track()
        return music_data['item']['name'] if music_data else "No song is playing"
