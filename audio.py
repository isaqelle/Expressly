# audio.py
import os
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5 import QtCore

class AudioPlayer:
    def __init__(self):
        self.media_player = QMediaPlayer() #creates an instance of QMediaPlayer, which will be used to handle media playback.

    def play_sound(self, sound_path): #sound_path (the file path of the sound)
            self.media_player.setMedia(QMediaContent(QtCore.QUrl.fromLocalFile(sound_path)))
            # Converts the given sound_path into a QUrl using QtCore.QUrl.fromLocalFile(sound_path), which ensures the file path is in the correct format.
            # Wraps the QUrl in a QMediaContent object and sets it as the media source for self.media_player.
            self.media_player.play() #Calls the .play() method on self.media_player, which starts playing the audio file.
