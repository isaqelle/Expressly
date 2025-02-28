import sys
import unittest
from unittest.mock import MagicMock
from PyQt5 import QtWidgets
from emojitavla import Ui_MainWindow
from calendar_1 import Ui_Form

# Run test
# python -m unittest discover -s tester -p "*.py"

class TestEmojiTavla(unittest.TestCase):

    # --------------------------------------------------------------
    # Set up the application and create the main window for testing.
    # Make sure QApplication is created only once for all tests
    # --------------------------------------------------------------
    @classmethod
    def setUpClass(cls):
        cls.app = QtWidgets.QApplication(sys.argv)  


    def setUp(self):
        self.main_window = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.main_window)
        self.ui.audio_player = MagicMock()

    # ------------------------------------------------------------------
    # Clean up after each test.
    # ------------------------------------------------------------------
    def tearDown(self):
        self.main_window.close()

    # ------------------------------------------------------------------
    # Test that the main window title is set correctly.
    # ------------------------------------------------------------------
    def test_main_window_title(self):
        self.assertEqual(self.main_window.windowTitle(), "Expressly")

    # ------------------------------------------------------------------
    # Test clicking the 'Very Happy' emoji button.
    # ------------------------------------------------------------------
    def test_very_happy_emoji_click(self):
        self.ui.veryHappyEmoji.click()  # Simulate button click
        self.ui.audio_player.play_sound.assert_called_once_with("audio_filer/VeryHappy.mp3")

    # ------------------------------------------------------------------
    # Test that clicking the calendar button opens the calendar window.
    # ------------------------------------------------------------------
    def test_open_calendar(self):
        self.ui.calendarButton.click()
        self.assertTrue(self.ui.calendar_window.isVisible())  # Check if the calendar window is visible

class TestCalendar(unittest.TestCase):

    # ------------------------------------------------------------------
    # Set up the application and create the calendar for testing.
    # ------------------------------------------------------------------
    def setUp(self):
        self.app = QtWidgets.QApplication(sys.argv)
        self.form_window = QtWidgets.QMainWindow()
        self.ui = Ui_Form()
        self.ui.setupUi(self.form_window)

    # ------------------------------------------------------------------
    # Clean up after each test.
    # ------------------------------------------------------------------
    def tearDown(self):
        self.form_window.close()

    # ------------------------------------------------------------------
    #  Test that the diary textbox has the correct placeholder text.
    # ------------------------------------------------------------------
    def test_diary_placeholder(self):       
        self.assertEqual(self.ui.diaryTextbox.placeholderText(), "Tell me about your day...")

   # ------------------------------------------------------------------
   # Test the save diary button functionality.
   # ------------------------------------------------------------------
    def test_save_button_functionality(self):

        self.ui.diaryTextbox.setPlainText("Test entry")
        self.ui.saveDiaryButton.click()

if __name__ == "__main__":
    unittest.main()
