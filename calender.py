from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(800, 600)
        Form.setFixedSize(800, 600)  # Keep window size fixed
        Form.setStyleSheet("background-color: rgb(232, 228, 214);")

        # Create the calendar widget
        self.calendarWidget = QtWidgets.QCalendarWidget(Form)
        self.calendarWidget.setGeometry(QtCore.QRect(30, 100, 350, 250))
        self.calendarWidget.setStyleSheet("background-color: rgb(211, 204, 186);")
        self.calendarWidget.setObjectName("calendarWidget")

        # Create the Save button
        self.pushButton_2 = QtWidgets.QPushButton(Form)
        self.pushButton_2.setGeometry(QtCore.QRect(410, 550, 350, 40))  # Wider button
        self.pushButton_2.setStyleSheet("font: 10pt \"MS Gothic\";\n"
                                        "color: rgb(255, 251, 225);\n"
                                        "background-color: #8caa9a")
        self.pushButton_2.setObjectName("pushButton_2")

        # Create the "CALENDAR" label
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(30, 10, 730, 70))  # Title bar
        self.label.setStyleSheet("font: 75 20pt \"MS Shell Dlg 2\";\n"
                                 "font: 36pt \"MS Shell Dlg 2\";\n"
                                 "color: #b9d9ba;\n"
                                 "background-color: #8caa9a;\n")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")

        # Create the "DIARY" label
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(410, 100, 350, 30))  # "DIARY"
        self.label_2.setStyleSheet("font: 15pt \"MS Shell Dlg 2\";\n"
                                   "color: #b9d9ba;\n"
                                   "background-color: #8caa9a")
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")

        # Create the Diary text box
        self.plainTextEdit_2 = QtWidgets.QPlainTextEdit(Form)
        self.plainTextEdit_2.setGeometry(QtCore.QRect(410, 130, 350, 410))
        self.plainTextEdit_2.setStyleSheet("background-color: rgb(211, 204, 186);")
        self.plainTextEdit_2.setObjectName("plainTextEdit_2")

        # Create the "ACTIVITIES" label
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(30, 380, 350, 30))  # "ACTIVITIES"
        self.label_3.setStyleSheet("font: 15pt \"MS Shell Dlg 2\";\n"
                                   "color: #b9d9ba;\n"
                                   "background-color: #8caa9a")
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")

        # Create the Activities text box
        self.plainTextEdit = QtWidgets.QPlainTextEdit(Form)
        self.plainTextEdit.setGeometry(QtCore.QRect(30, 380, 350, 160))
        self.plainTextEdit.setStyleSheet("background-color: rgb(211, 204, 186);")
        self.plainTextEdit.setObjectName("plainTextEdit")

        # New button to open a new window (dialog)
        self.openWindowButton = QtWidgets.QPushButton(Form)
        self.openWindowButton.setGeometry(QtCore.QRect(30, 380 + 160 + 10, 350, 40))  # Below the calendar and activities
        self.openWindowButton.setText("Add activity")
        self.openWindowButton.setStyleSheet("font: 10pt \"MS Gothic\";\n"
                                            "color: rgb(255, 251, 225);\n"
                                            "background-color: #8caa9a")
        self.openWindowButton.setObjectName("openWindowButton")

        # Connect the button to open the new window
        self.openWindowButton.clicked.connect(self.openNewWindow)

        self.calendarWidget.raise_()
        self.label.raise_()
        self.plainTextEdit.raise_()
        self.plainTextEdit_2.raise_()
        self.label_2.raise_()
        self.pushButton_2.raise_()
        self.label_3.raise_()

        # Save the diary entries in a dictionary with the date as the key
        self.diary_entries = {}

        # Connect the Save button to the save function
        self.pushButton_2.clicked.connect(self.saveDiaryEntry)

        # Connect the calendar date selection to load the diary entry for that date
        self.calendarWidget.selectionChanged.connect(self.loadDiaryEntry)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def saveDiaryEntry(self):
        selected_date = self.calendarWidget.selectedDate()
        formatted_date = selected_date.toString("yyyy-MM-dd")  # Format the date as "yyyy-MM-dd"
        
        diary_text = self.plainTextEdit_2.toPlainText()
        self.diary_entries[formatted_date] = diary_text
        print(f"Diary entry saved for {formatted_date}: {diary_text}")
    
    def loadDiaryEntry(self):
        selected_date = self.calendarWidget.selectedDate()
        formatted_date = selected_date.toString("yyyy-MM-dd")
        
        if formatted_date in self.diary_entries:
            self.plainTextEdit_2.setPlainText(self.diary_entries[formatted_date])
        else:
            self.plainTextEdit_2.clear()  # Clear text if no entry exists for that date

    def openNewWindow(self):
        # Create a new dialog window
        self.dialog = QtWidgets.QDialog()
        self.dialog.setWindowTitle("New Window")
        self.dialog.resize(400, 300)

        # Add a label to the new window
        label = QtWidgets.QLabel(self.dialog)
        label.setText("This is a new window!")
        label.setGeometry(100, 100, 200, 40)

        # Show the new window
        self.dialog.exec_()

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.pushButton_2.setText(_translate("Form", "Save Changes"))
        self.label.setText(_translate("Form", "CALENDAR"))
        self.label_2.setText(_translate("Form", "DIARY"))
        self.plainTextEdit_2.setPlaceholderText(_translate("Form", "Tell me about your day..."))
        self.label_3.setText(_translate("Form", "ACTIVITIES"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
