import sys
import os
import unittest
import firebase_admin
from firebase_admin import credentials, firestore

# Short path fix: go one level up so we can import emojitavla.py
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtTest import QTest
from PyQt5.QtCore import Qt

from emojitavla import Ui_MainWindow  # Main UI with emojis, buttons, etc.
from audio import AudioPlayer  # AudioPlayer class

class IntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Initialize QApplication and Firebase once for all tests."""
        cls.app = QApplication(sys.argv)
        if not firebase_admin._apps:
            # Adjust the path if serviceAccountKey.json is elsewhere
            cred_path = os.path.join(parent_dir, "serviceAccountKey.json")
            cred = credentials.Certificate(cred_path)
            firebase_admin.initialize_app(cred)
        cls.db = firestore.client()

    def setUp(self):
        """Create the main window and mock the audio player's play_sound."""
        self.window = QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.window)
        self.window.show()

        # Mock audio to verify playback without playing real sound
        self.audio_called = False
        def fake_play_sound(file_path):
            self.audio_called = True
            self.called_file = file_path
        self.original_play_sound = self.ui.audio_player.play_sound
        self.ui.audio_player.play_sound = fake_play_sound

    def tearDown(self):
        """Restore original audio method and close the window."""
        self.ui.audio_player.play_sound = self.original_play_sound
        self.window.close()

    def test_audio_integration(self):
        """Check if clicking an emoji triggers audio playback."""
        # Simulate a click on the happy emoji
        QTest.mouseClick(self.ui.happyEmoji, Qt.LeftButton)
        self.assertTrue(self.audio_called, "Audio should have been triggered.")
        self.assertEqual(self.called_file, "audio_filer/Happy.mp3", "Incorrect audio file called.")

    def test_firebase_integration(self):
        """Check if data can be saved and retrieved from Firestore."""
        test_ref = self.db.collection("calendar_entries").document("integration_test_doc")
        test_data = {
            "diary": "Integration test diary",
            "activities": "Integration test activity (Energy: 5/10)"
        }
        test_ref.set(test_data)
        result = test_ref.get().to_dict()
        self.assertEqual(result.get("diary"), "Integration test diary", "Diary data mismatch.")
        self.assertEqual(result.get("activities"), "Integration test activity (Energy: 5/10)", "Activities mismatch.")

    def test_calendar_opening(self):
        """Check if clicking the calendar button opens the calendar window."""
        QTest.mouseClick(self.ui.calendarButton, Qt.LeftButton)
        # openCalendar() should create self.calendar_window in Ui_MainWindow
        self.assertTrue(hasattr(self.ui, "calendar_window"), "Calendar window should be created.")
        self.assertTrue(self.ui.calendar_window.isVisible(), "Calendar window should be visible.")

if __name__ == '__main__':
    unittest.main()
