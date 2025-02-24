import unittest
from PyQt5.QtWidgets import QApplication, QWidget
from emojitavla import Ui_Form  # Make sure this points to your UI class

class TestUI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication([])  # Create a QApplication instance
        cls.window = QWidget()  # Create a QWidget instance
        cls.ui = Ui_Form()  # Initialize your UI class
        cls.ui.setupUi(cls.window)  # Set up the UI with the QWidget

    def test_add_activity_button_exists(self):
        self.assertIsNotNone(self.ui.addActivityButton, "Add Activity button should exist")

    def test_save_button_exists(self):
        self.assertIsNotNone(self.ui.saveDiaryButton, "Save Changes button should exist")

    def test_activity_textbox_initialization(self):
        self.assertEqual(self.ui.plainTextEdit.toPlainText(), "No added activities yet...", "Initial text should match placeholder")

    def test_diary_textbox_initialization(self):
        self.assertEqual(self.ui.diaryTextbox.toPlainText(), "", "Diary textbox should be empty initially")

    def test_calendar_label_exists(self):
        self.assertIsNotNone(self.ui.calendarLabel, "Calendar label should exist")

if __name__ == '__main__':
    unittest.main()
