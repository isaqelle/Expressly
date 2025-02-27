import os
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5 import QtCore

# ------------------------------
# SECTION: Audio Player
# Manages the audio playing when pressing the emojis
# ------------------------------

class AudioPlayer:
    def __init__(self):
        self.mediaPlayer = QMediaPlayer() #creates an instance of QMediaPlayer, which will be used to handle media playback.

    def playSound(self, soundPath): #sound_path (the file path of the sound)
            self.mediaPlayer.setMedia(QMediaContent(QtCore.QUrl.fromLocalFile(soundPath)))
            # Converts the given sound_path into a QUrl using QtCore.QUrl.fromLocalFile(sound_path), which ensures the file path is in the correct format.
            # Wraps the QUrl in a QMediaContent object and sets it as the media source for self.media_player.
            self.mediaPlayer.play() #Calls the .play() method on self.media_player, which starts playing the audio file.
