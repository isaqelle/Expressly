import os
import firebase_admin
from firebase_admin import credentials, firestore
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPainter, QColor, QFont, QPixmap, QIcon
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtWidgets import QApplication, QPushButton, QWidget, QHBoxLayout, QVBoxLayout
from PyQt5.QtWidgets import QSpacerItem, QSizePolicy
from PyQt5.QtCore import QSettings

# Some debugging code, checking the current working directory and verifying that "serviceAccountKey.json" existis
print("Current working directory:", os.getcwd())
print("Checking if serviceAccountKey.json exists:", os.path.isfile("serviceAccountKey.json"))

# ------------------------------
# SECTION: User ID
# Finds user ID from the settings file
# ------------------------------
settings = QSettings("HKEY_CURRENT_USER\\Software\\Expressly\\Expressly", QSettings.NativeFormat)
UserId = settings.value("uid")

# ------------------------------
# SECTION: Battery Widget
# Paints up the battery using QPainter and QColor
# ------------------------------
class BatteryWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.energyLevel = 0  
        self.setFixedSize(300, 150)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Setting size of the battery
        batteryX, batteryY, batteryWidth, batteryHeight = 30, 40, 200, 60
        # Draw battery outline
        painter.setPen(Qt.black)
        painter.drawRect(batteryX, batteryY, batteryWidth, batteryHeight)
        painter.drawRect(batteryX + batteryWidth, batteryY + 20, 10, 20)  

        # Fill battery
        if self.energyLevel > 0:
            fillWidth = int(batteryWidth * (self.energyLevel / 10))
            fillColor = self.getEnergyColor(self.energyLevel)
            painter.setBrush(QColor(fillColor))
            painter.drawRect(batteryX, batteryY, fillWidth, batteryHeight)
        else:
            painter.setBrush(QColor("#D3D3D3"))  
            painter.drawRect(batteryX, batteryY, batteryWidth, batteryHeight)

        # "Energy level" text
        painter.setFont(QFont("Arial", 14, QFont.Bold))
        painter.setPen(Qt.black)
        painter.drawText(batteryX, batteryY + 90, f"Energy level: {self.energyLevel}/10")  # Align text with battery

    def mousePressEvent(self, event):
        self.updateEnergyLevel(event.x())

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.updateEnergyLevel(event.x())

    # The battery level
    def updateEnergyLevel(self, xPosition):
        batteryLeft, batteryRight = 30, 220
        if batteryLeft <= xPosition <= batteryRight:
            self.energyLevel = max(0, min(int((xPosition - batteryLeft) / (batteryRight - batteryLeft) * 10), 10))
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
        self.activitiesTextbox = QtWidgets.QPlainTextEdit(Form)
        self.activitiesTextbox.setGeometry(30, 410, 350, 130)
        self.activitiesTextbox.setStyleSheet("background-color: rgb(211, 204, 186);")
        self.activitiesTextbox.setPlaceholderText("No added activities yet...")

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
        self.addActivityButton.clicked.connect(self.openActivityWindow)
        self.updateTextFields()

# ------------------------------
# SECTION: "Add activity" window
# ------------------------------

    def openActivityWindow(self):
        self.ActivityDialog = QtWidgets.QDialog()
        self.ActivityDialog.setWindowTitle("New Activity")
        self.ActivityDialog.setFixedSize(450, 600)
        self.ActivityDialog.setStyleSheet("background-color: rgb(232, 228, 214);")


        layoutMain = QVBoxLayout()

        activityLabel = QtWidgets.QLabel("Activity:")
        layoutMain.addWidget(activityLabel)

        self.activityInput = QtWidgets.QLineEdit()
        layoutMain.addWidget(self.activityInput)

        energyLabel = QtWidgets.QLabel("Energybattery:")
        layoutMain.addWidget(energyLabel)

        self.battery = BatteryWidget()
        layoutMain.addWidget(self.battery)
        
        emojiLabel = QtWidgets.QLabel("Mood:")
        layoutMain.addWidget(emojiLabel)

        layoutEmoji = QHBoxLayout()

        # Horizontal layout for emoji images
        self.imageLayout = QHBoxLayout()
        self.emojiImagePaths = [
            "images/grinning-face-with-big-eyes_1f603.png", "images/slightly-smiling-face_1f642.png", "images/neutral-face_1f610.png",
            "images/crying-face_1f622.png", "images/sleeping-face_1f634.png", "images/pouting-face_1f621.png"
        ]

        self.emojiButtons = []

        for path in self.emojiImagePaths:
            button = QPushButton()
            button.setIcon(QIcon(path))
            button.setIconSize(QtCore.QSize(50, 50))  # The size 
            button.setStyleSheet("border: 2px solid transparent;")  # Default style
            button.clicked.connect(lambda checked, b=button: self.selectImage(b))
            self.imageLayout.addWidget(button)
            self.emojiButtons.append(button)

        layoutEmoji.addLayout(self.imageLayout)
        layoutMain.addLayout(layoutEmoji) 

        spacer = QSpacerItem(10, 15, QSizePolicy.Minimum, QSizePolicy.Fixed)
        layoutMain.addItem(spacer)


        self.saveActivityButton = QtWidgets.QPushButton("Save Activity")
        self.saveActivityButton.setStyleSheet("font: 10pt \"MS Gothic\";\ncolor: rgb(255, 251, 225);\nbackground-color: #8caa9a")
        self.saveActivityButton.clicked.connect(self.saveActivity)
        layoutMain.addWidget(self.saveActivityButton)

        self.ActivityDialog.setLayout(layoutMain)
        self.ActivityDialog.exec_()

    def selectImage(self, selectedButton):
        for button in self.emojiButtons:
            button.setStyleSheet("border: 2px solid transparent;")
        
        selectedButton.setStyleSheet("border: 2px solid green;")

        # Dictionary that links each emoji button to a mood
        moodMap = {
            self.emojiButtons[0]: "veryHappy",
            self.emojiButtons[1]: "happy",
            self.emojiButtons[2]: "neutral",
            self.emojiButtons[3]: "sad",
            self.emojiButtons[4]: "tired",
            self.emojiButtons[5]: "angry"
        }
        
        self.selectedMood = moodMap.get(selectedButton, "neutral")
# ------------------------------
# SECTION: Save the data from "Add activity" window
# ------------------------------

    def saveData(self):
        selectedDate = self.calendarWidget.selectedDate().toString(QtCore.Qt.ISODate)
        diaryText = self.diaryTextbox.toPlainText()
        activitiesText = self.activitiesTextbox.toPlainText()

        cleanedActivities = "\n".join([line for line in activitiesText.split("\n") if line.strip()])

        try:
            # Get reference to Firestore
            docRef = db.collection("users").document(UserId).collection("calendar_entries").document(selectedDate)

            # Save whats in GUI to firestore
            data = {
                "diary": diaryText,
                "activities": cleanedActivities
            }

            docRef.set(data)  # Send data to Firestore
            self.activitiesTextbox.setPlainText(cleanedActivities)  # Update GUI without empty lines

            print(f"Data saved for {selectedDate}")  # Debugging

        except Exception as e:
            print(f"Failed to save data: {e}")  # Debugging


    # Save activities  without deleting diary
    def saveActivity(self):
        activityText = self.activityInput.text()
        energyLevel = self.battery.energyLevel
        selectedDate = self.calendarWidget.selectedDate().toString(QtCore.Qt.ISODate)

        if activityText.strip():
            moodEmoji = {  
                "veryHappy": "ヽ(◕‿◕｡)ノ",
                "happy": "(◕‿◕)",  
                "neutral": "ヽ(ー_ー )ノ",  
                "sad": "(╯︵╰,)",
                "tired": "(－_－) zzZ",
                "angry": "ヽ( `д´*)ノ"
            }.get(self.selectedMood, "")  

            entry = f"{activityText} (Energy: {energyLevel}/10) {moodEmoji}\n"


            emojiLabel = QtWidgets.QLabel()
            if hasattr(self, 'selectedEmoji'):
                self.selectedEmoji = None

                # Create an entry widget with emoji and text
                entryWidget = QtWidgets.QWidget()
                entryLayout = QHBoxLayout(entryWidget)
                entryLayout.addWidget(QtWidgets.QLabel(entry))  # Activity text
                entryLayout.addWidget(emojiLabel)  # Add emoji
                entryLayout.addStretch()
                entryLayout.setContentsMargins(0, 0, 0, 0)

            try:
                # Get refenrece to Firestore
                doc_ref = db.collection("users").document(UserId).collection("calendar_entries").document(selectedDate)
                existingData = doc_ref.get().to_dict() or {"diary": "", "activities": ""}

                # Add activity
                updatedActivities = (existingData.get("activities", "") + "\n" + entry).strip()

                # Update Firestore
                doc_ref.set({
                    "diary": existingData["diary"],  
                    "activities": updatedActivities
                })

                self.activitiesTextbox.setPlainText(updatedActivities)  # Update GUI
                self.ActivityDialog.close()  # Close activity window

                print(f"Activity saved for {selectedDate}")  # Debugging

            except Exception as e:
                print(f"Failed to save activity: {e}")  # Debugging

    # Get data from Firebase
    def updateTextFields(self):
        selectedDate = self.calendarWidget.selectedDate().toString(QtCore.Qt.ISODate)

        try:
            doc_ref = db.collection("users").document(UserId).collection("calendar_entries").document(selectedDate)
            data = doc_ref.get().to_dict()

            if data:
                self.diaryTextbox.setPlainText(data.get("diary", ""))
                self.activitiesTextbox.setPlainText(data.get("activities", ""))
            else:
                self.diaryTextbox.clear()
                self.activitiesTextbox.clear()

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