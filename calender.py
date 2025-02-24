import os
import firebase_admin
from firebase_admin import credentials, firestore
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPainter, QColor, QFont
from PyQt5.QtCore import Qt, QDate

# Some debugging code, checking the current working directory and verifying that "serviceAccountKey.json" existis
print("Current working directory:", os.getcwd())
print("Checking if serviceAccountKey.json exists:", os.path.isfile("serviceAccountKey.json"))


# ------------------------------
# SECTION: Battery Widget
# Paints up the battery using QPainter and QColor
# ------------------------------
class BatteryWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.energy_level = 0  
        self.setFixedSize(300, 150)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Setting size of the battery
        battery_x, battery_y, battery_width, battery_height = 30, 40, 200, 60
        # Draw battery outline
        painter.setPen(Qt.black)
        painter.drawRect(battery_x, battery_y, battery_width, battery_height)
        painter.drawRect(battery_x + battery_width, battery_y + 20, 10, 20)  

        # Fill battery
        if self.energy_level > 0:
            fill_width = int(battery_width * (self.energy_level / 10))
            fill_color = self.getEnergyColor(self.energy_level)
            painter.setBrush(QColor(fill_color))
            painter.drawRect(battery_x, battery_y, fill_width, battery_height)
        else:
            painter.setBrush(QColor("#D3D3D3"))  
            painter.drawRect(battery_x, battery_y, battery_width, battery_height)

        # "Energy level" text
        painter.setFont(QFont("Arial", 14, QFont.Bold))
        painter.setPen(Qt.black)
        painter.drawText(battery_x, battery_y + 90, f"Energy level: {self.energy_level}/10")  # Align text with battery

    def mousePressEvent(self, event):
        self.updateEnergyLevel(event.x())

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.updateEnergyLevel(event.x())

    def updateEnergyLevel(self, x_position):
        battery_left, battery_right = 30, 220
        if battery_left <= x_position <= battery_right:
            self.energy_level = max(0, min(int((x_position - battery_left) / (battery_right - battery_left) * 10), 10))
            self.update()

    # Setting the colors in the battery
    def getEnergyColor(self, value):
        if value == 0:
            return "#D3D3D3"  # Default color/ empty battery color, lightgray
        elif value <= 3:
            return "#ea9789"  # Red (low energy, from 3 or lower)
        elif value <= 7:
            return "#eaca97"  # Orange (medium energy, from 7 or lower)
        else:
            return "#86c077"  # Green (high anergy, over 7)

# ------------------------------
# SECTION: Firebase
# Initialize Firebase using service account credentials and create a Firestore client to interact with the database.
# ------------------------------

if not firebase_admin._apps:
    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred)

db = firestore.client() 

# ------------------------------
# SECTION: Calender Window
# ------------------------------

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(800, 600)
        Form.setFixedSize(800, 600)
        Form.setStyleSheet("background-color: rgb(232, 228, 214);")

        # Calendar Label ("CALENDAR" title)
        self.calendarLabel = QtWidgets.QLabel(Form)
        self.calendarLabel.setGeometry(30, 10, 730, 70)
        self.calendarLabel.setStyleSheet("font: 36pt \"MS Shell Dlg 2\";\ncolor: #b9d9ba;\nbackground-color: #8caa9a;")
        self.calendarLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.calendarLabel.setText("CALENDAR")

        # Displays the calendar
        self.calendarWidget = QtWidgets.QCalendarWidget(Form)
        self.calendarWidget.setGeometry(30, 100, 350, 250)
        self.calendarWidget.setStyleSheet("background-color: rgb(211, 204, 186);")
        self.calendarWidget.selectionChanged.connect(self.updateTextFields)

        # Diary Label ("DIARY" title)
        self.diaryLabel = QtWidgets.QLabel(Form)
        self.diaryLabel.setGeometry(410, 100, 350, 30)
        self.diaryLabel.setStyleSheet("font: 15pt \"MS Shell Dlg 2\";\ncolor: #b9d9ba;\nbackground-color: #8caa9a")
        self.diaryLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.diaryLabel.setText("DIARY")

        # Diary textbox
        self.diaryTextbox = QtWidgets.QPlainTextEdit(Form)
        self.diaryTextbox.setGeometry(410, 130, 350, 410)
        self.diaryTextbox.setStyleSheet("background-color: rgb(211, 204, 186);")
        self.diaryTextbox.setPlaceholderText("Tell me about your day...")

        # Activities label ("ACTIVITIES" title)
        self.activitiesLabel = QtWidgets.QLabel(Form)
        self.activitiesLabel.setGeometry(30, 380, 350, 30)
        self.activitiesLabel.setStyleSheet("font: 15pt \"MS Shell Dlg 2\";\ncolor: #b9d9ba;\nbackground-color: #8caa9a")
        self.activitiesLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.activitiesLabel.setText("ACTIVITIES")

        # Activities textbox
        self.plainTextEdit = QtWidgets.QPlainTextEdit(Form)
        self.plainTextEdit.setGeometry(30, 410, 350, 130)
        self.plainTextEdit.setStyleSheet("background-color: rgb(211, 204, 186);")
        self.plainTextEdit.setPlaceholderText("No added activities yet...")

        # Save Changes button
        self.saveDiaryButton = QtWidgets.QPushButton(Form)
        self.saveDiaryButton.setGeometry(410, 550, 350, 40)
        self.saveDiaryButton.setStyleSheet("font: 10pt \"MS Gothic\";\ncolor: rgb(255, 251, 225);\nbackground-color: #8caa9a")
        self.saveDiaryButton.setText("Save Changes")
        self.saveDiaryButton.clicked.connect(self.saveData)

        # Add activity button
        self.addActivityButton = QtWidgets.QPushButton(Form)
        self.addActivityButton.setGeometry(30, 550, 350, 40)
        self.addActivityButton.setText("Add Activity")
        self.addActivityButton.setStyleSheet("font: 10pt \"MS Gothic\";\ncolor: rgb(255, 251, 225);\nbackground-color: #8caa9a")
        self.addActivityButton.clicked.connect(self.openNewWindow)
        self.updateTextFields()

# ------------------------------
# SECTION: "Add activity" window
# ------------------------------

    def openNewWindow(self):
        self.dialog = QtWidgets.QDialog()
        self.dialog.setWindowTitle("New Activity")
        self.dialog.setFixedSize(300, 350)

        layout = QtWidgets.QVBoxLayout()

        activity_label = QtWidgets.QLabel("Activity:")
        
        layout.addWidget(activity_label)

        self.activity_input = QtWidgets.QLineEdit()
        layout.addWidget(self.activity_input)

        energy_label = QtWidgets.QLabel("Energybattery:")
        layout.addWidget(energy_label)

        self.battery = BatteryWidget()
        layout.addWidget(self.battery)

        self.save_button = QtWidgets.QPushButton("Save Activity")
        self.save_button.setStyleSheet("font: 10pt \"MS Gothic\";\ncolor: rgb(255, 251, 225);\nbackground-color: #8caa9a")
        self.save_button.clicked.connect(self.saveActivity)
        layout.addWidget(self.save_button)

        self.dialog.setLayout(layout)
        self.dialog.exec_()

# ------------------------------
# SECTION: Save the data from "Add activity" window
# ------------------------------

    def saveData(self):
        selected_date = self.calendarWidget.selectedDate().toString(QtCore.Qt.ISODate)
        diary_text = self.diaryTextbox.toPlainText()
        activities_text = self.plainTextEdit.toPlainText()

        cleaned_activities = "\n".join([line for line in activities_text.split("\n") if line.strip()])

        try:
            # Get reference to Firestore
            doc_ref = db.collection("calendar_entries").document(selected_date)

            # Save whats in GUI to firestore
            data = {
                "diary": diary_text,
                "activities": cleaned_activities
            }

            doc_ref.set(data)  # Send data to Firestore
            self.plainTextEdit.setPlainText(cleaned_activities)  # Update GUI without empty lines

            print(f"Data saved for {selected_date}")  # Debugging

        except Exception as e:
            print(f"Failed to save data: {e}")  # Debugging


    # Save activities  without deleting diary
    def saveActivity(self):
        activity_text = self.activity_input.text()
        energy_level = self.battery.energy_level
        selected_date = self.calendarWidget.selectedDate().toString(QtCore.Qt.ISODate)

        if activity_text.strip():
            entry = f"{activity_text} (Energy: {energy_level}/10)\n"

            try:
                # Get refenrece to Firestore
                doc_ref = db.collection("calendar_entries").document(selected_date)
                existing_data = doc_ref.get().to_dict() or {"diary": "", "activities": ""}

                # Add activity
                updated_activities = existing_data["activities"] + entry if existing_data["activities"] else entry

                # Update Firestore
                doc_ref.set({
                    "diary": existing_data["diary"],  
                    "activities": updated_activities
                })

                self.plainTextEdit.setPlainText(updated_activities)  # Update GUI
                self.dialog.close()  # Close activity window

                print(f"Activity saved for {selected_date}")  # Debugging

            except Exception as e:
                print(f"Failed to save activity: {e}")  # Debugging

    # Get data from Firebase
    def updateTextFields(self):
        selected_date = self.calendarWidget.selectedDate().toString(QtCore.Qt.ISODate)

        try:
            doc_ref = db.collection("calendar_entries").document(selected_date)
            data = doc_ref.get().to_dict()

            if data:
                self.diaryTextbox.setPlainText(data.get("diary", ""))
                self.plainTextEdit.setPlainText(data.get("activities", ""))
            else:
                self.diaryTextbox.clear()
                self.plainTextEdit.clear()

        except Exception as e:
            print(f" Failed to load data: {e}")  # Debugging

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())