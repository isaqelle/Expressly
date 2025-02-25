import sys
import unittest
from PyQt5 import QtWidgets
from emojitavla import Ui_MainWindow
from calendar_1 import Ui_Form

class TestEmojiTavla(unittest.TestCase):

    def setUp(self):
        """Set up the application and create the main window for testing."""
        self.app = QtWidgets.QApplication(sys.argv)
        self.main_window = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.main_window)

    def tearDown(self):
        """Clean up after each test."""
        self.main_window.close()

    def test_main_window_title(self):
        """Test that the main window title is set correctly."""
        self.assertEqual(self.main_window.windowTitle(), "Expressly")

    def test_very_happy_emoji_click(self):
        """Test clicking the 'Very Happy' emoji button."""
        self.ui.veryHappyEmoji.click()  # Simulate button click
     
    def test_open_calendar(self):
        """Test that clicking the calendar button opens the calendar window."""
        self.ui.calendarButton.click()
        self.assertTrue(self.ui.calendar_window.isVisible())  # Check if the calendar window is visible

class TestCalendar(unittest.TestCase):

    def setUp(self):
        """Set up the application and create the calendar for testing."""
        self.app = QtWidgets.QApplication(sys.argv)
        self.form_window = QtWidgets.QMainWindow()
        self.ui = Ui_Form()
        self.ui.setupUi(self.form_window)

    def tearDown(self):
        """Clean up after each test."""
        self.form_window.close()

    def test_diary_placeholder(self):
        """Test that the diary textbox has the correct placeholder text."""
        self.assertEqual(self.ui.diaryTextbox.placeholderText(), "Tell me about your day...")

    def test_save_button_functionality(self):
        """Test the save diary button functionality."""
        self.ui.diaryTextbox.setPlainText("Test entry")
        self.ui.saveDiaryButton.click() 

if __name__ == "__main__":
    unittest.main()

# python -m unittest discover -s tester -p "*.py"   