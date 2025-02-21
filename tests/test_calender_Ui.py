import pytest
import os
import sys
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtTest import QTest
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from calender import Ui_Form

@pytest.fixture
def main_form():
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    yield ui
    app.quit()

def test_save_changes(main_form):
    QTest.keyClicks(main_form.plainTextEdit_2, "Today was a good day.")

    QTest.mouseClick(main_form.pushButton_2, Qt.LeftButton)
    selected_date = main_form.calendarWidget.selectedDate().toString(Qt.ISODate)
    assert main_form.data_store[selected_date]["diary"] == "Today was a good day."

def test_add_activity(main_form):
    #Click the acitivity button
    QTest.mouseClick(main_form.openWindowButton, Qt.LeftButton)
    
