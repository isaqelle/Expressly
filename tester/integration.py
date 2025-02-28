import sys
import os
import unittest
import firebase_admin
from firebase_admin import credentials, firestore

# ------------------------------
# SECTION: Path Configuration
# Short path fix: go one level up so we can import emojitavla.py
# ------------------------------
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtTest import QTest
from PyQt5.QtCore import Qt

# ------------------------------
# SECTION: Import UI and Audio Player
# ------------------------------
from emojitavla import uiMainWindow  # Main UI with emojis, buttons, etc.
from audio import AudioPlayer  # AudioPlayer class

# ------------------------------
# SECTION: Integration Tests
# ------------------------------
class IntegrationTests(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        """Initialize QApplication and Firebase once for all tests."""
        cls.app = QApplication(sys.argv)

        # Initialize Firebase if not already initialized
        if not firebase_admin._apps:
            cred_path = os.path.join(parent_dir, "serviceAccountKey.json")  # Adjust path if needed
            cred = credentials.Certificate(cred_path)
            firebase_admin.initialize_app(cred)
        
        cls.db = firestore.client()  # Firestore database connection

    def setUp(self):
        """Create the main window and mock the audio player's play_sound method."""
        self.window = QMainWindow()
        self.ui = uiMainWindow()
        self.ui.setupUi(self.window)
        self.window.show()

        # Mock audio player to verify playback without actual sound
        self.audio_called = False
        def fake_play_sound(file_path):
            self.audio_called = True
            self.called_file = file_path
        
        self.original_play_sound = self.ui.audioPlayer.playSound
        self.ui.audioPlayer.playSound = fake_play_sound  # Replace actual function with mock

    def tearDown(self):
        """Restore original audio method and close the window."""
        self.ui.audioPlayer.playSound = self.original_play_sound
        self.window.close()

    # ------------------------------
    # TEST: Audio Integration
    # ------------------------------
    def test_audio_integration(self):
        """Check if clicking an emoji triggers audio playback."""
        # Simulate a click on the happy emoji
        QTest.mouseClick(self.ui.happyEmoji, Qt.LeftButton)
        
        # Verify that the playSound function was triggered
        self.assertTrue(self.audio_called, "Audio should have been triggered.")
        self.assertEqual(self.called_file, "audio_filer/Happy.mp3", "Incorrect audio file called.")

    # ------------------------------
    # TEST: Firebase Integration
    # ------------------------------
    def test_firebase_integration(self):
        """Check if data can be saved and retrieved from Firestore."""
        test_ref = self.db.collection("calendar_entries").document("integration_test_doc")

        # Test data to store in Firestore
        test_data = {
            "diary": "Integration test diary",
            "activities": "Integration test activity (Energy: 5/10)"
        }

        # Store and retrieve the data
        test_ref.set(test_data)
        result = test_ref.get().to_dict()

        # Verify that the data matches
        self.assertEqual(result.get("diary"), "Integration test diary", "Diary data mismatch.")
        self.assertEqual(result.get("activities"), "Integration test activity (Energy: 5/10)", "Activities mismatch.")

    # ------------------------------
    # TEST: Calendar Opening
    # ------------------------------
    def test_calendar_opening(self):
        """Check if clicking the calendar button opens the calendar window."""
        QTest.mouseClick(self.ui.calendarButton, Qt.LeftButton)

        # Verify that the calendar window is created and visible
        self.assertTrue(hasattr(self.ui, "calendarWindow"), "Calendar window should be created.")
        self.assertTrue(self.ui.calendarWindow.isVisible(), "Calendar window should be visible.")

# ------------------------------
# SECTION: Run Tests
# ------------------------------
if __name__ == '__main__':
    unittest.main()

