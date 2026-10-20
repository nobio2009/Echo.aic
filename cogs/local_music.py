import os
import random
from pathlib import Path

import pygame


class LocalMusicPlayer:
    current = 0

    def __init__(self):
        self.folder = str(Path(__file__).resolve().parents[1] / "local_music")
        self.mp3s = [f for f in os.listdir(self.folder) if f.endswith(".mp3")]
        random.shuffle(self.mp3s)

        pygame.mixer.init()

    def play(self):
        current_song = os.path.join(self.folder, self.mp3s[self.current])
        pygame.mixer.music.load(current_song)
        pygame.mixer.music.play()

        print(self.mp3s)

    def pause(self):
        pygame.mixer.music.stop()

    def skip(self):
        print(f'len: {len(self.mp3s)}, current index: {self.current}')
        self.current =+ 1
        if self.current >= len(self.mp3s):
            self.current = 0
        self.play()
        print(self.current)
        print(f'{os.path.join(self.folder, self.mp3s[self.current])}')
