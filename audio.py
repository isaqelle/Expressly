# audio.py
import os
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5 import QtCore

class AudioPlayer:
    def __init__(self):
        self.media_player = QMediaPlayer()

    def play_sound(self, sound_path):
            self.media_player.setMedia(QMediaContent(QtCore.QUrl.fromLocalFile(sound_path)))
            self.media_player.play()
