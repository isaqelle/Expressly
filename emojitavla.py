from PyQt5 import QtCore, QtGui, QtWidgets
import requests
from audio import AudioPlayer
from PyQt5.QtCore import QSettings
from calendar_1 import Ui_Form
from statistics_1 import TrendOverviewWindow, getTrendDataFromFirebase

# ------------------------------
# SECTION: MainWindow
# ------------------------------
class uiMainWindow(object):
    def setupUi(self, MainWindow):
        """ Sets up the main window UI """
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(500, 400)
        MainWindow.setMaximumSize(QtCore.QSize(500, 400))
        MainWindow.setStyleSheet("QMainWindow {\n"
                                 "    background-color: rgb(185, 217, 186);\n"
                                 "}\n"
                                 "")

        self.audioPlayer = AudioPlayer()
        MainWindow.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # ------------------------------
        # SECTION: Emoji Table 
        # ------------------------------
        self.emojiTable = QtWidgets.QFrame(self.centralwidget)
        self.emojiTable.setGeometry(QtCore.QRect(280, 60, 161, 241))
        self.emojiTable.setStyleSheet("QFrame {\n"
                                      "background-color: rgb(232, 228, 214);\n"
                                      "border: 2px solid black;\n"
                                      "border-radius: 10px;\n"
                                      "}")
        self.emojiTable.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.emojiTable.setFrameShadow(QtWidgets.QFrame.Raised)
        self.emojiTable.setObjectName("emojiTable")

        self.gridLayout = QtWidgets.QGridLayout(self.emojiTable)
        self.gridLayout.setContentsMargins(5, 5, 5, 5)
        self.gridLayout.setSpacing(10)

        emoji_icons = {
            "veryHappy": "bilder/grinning-face-with-big-eyes_1f603.png",
            "happy": "bilder/slightly-smiling-face_1f642.png",
            "sad": "bilder/crying-face_1f622.png",
            "neutral": "bilder/neutral-face_1f610.png",
            "angry": "bilder/pouting-face_1f621.png",
            "tired": "bilder/sleeping-face_1f634.png"
        }

        emoji_sounds = {
            "veryHappy": "audio_filer/VeryHappy.mp3",
            "happy": "audio_filer/Happy.mp3",
            "sad": "audio_filer/Sad.mp3",
            "neutral": "audio_filer/Neutral.mp3",
            "angry": "audio_filer/Angry.mp3",
            "tired": "audio_filer/Tired.mp3"
        }

        emoji_positions = [(0, 0), (0, 1), (1, 0), (1, 1), (2, 0), (2, 1)]
        emoji_keys = list(emoji_icons.keys())

        self.emojiButtons = {}
        for i, key in enumerate(emoji_keys):
            self.emojiButtons[key] = QtWidgets.QPushButton(self.emojiTable)
            self.emojiButtons[key].setText("")
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap(emoji_icons[key]), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.emojiButtons[key].setIcon(icon)
            self.emojiButtons[key].setIconSize(QtCore.QSize(55, 55))
            self.emojiButtons[key].setFixedSize(60, 60)
            self.emojiButtons[key].setFlat(True)
            self.emojiButtons[key].setObjectName(key)
            self.gridLayout.addWidget(self.emojiButtons[key], *emoji_positions[i])

            self.emojiButtons[key].clicked.connect(lambda _, sound=emoji_sounds[key]: self.audioPlayer.playSound(sound))

        # ------------------------------
        # SECTION: "Today" button
        # ------------------------------
        self.TodaysCalander = QtWidgets.QFrame(self.centralwidget)
        self.TodaysCalander.setGeometry(QtCore.QRect(70, 60, 121, 111))
        self.TodaysCalander.setStyleSheet("QFrame {\n"
                                          "background-color: rgb(232, 228, 214);\n"
                                          "border: 2px solid black;\n"
                                          "border-radius: 10px;\n"
                                          "}")
        self.TodaysCalander.setObjectName("TodaysCalander")

        self.todayButton = QtWidgets.QPushButton(self.TodaysCalander)
        self.todayButton.setGeometry(QtCore.QRect(20, 20, 81, 71))
        self.todayButton.setText("")
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap("bilder/Today.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.todayButton.setIcon(icon6)
        self.todayButton.setIconSize(QtCore.QSize(125, 50))
        self.todayButton.setFlat(True)
        self.todayButton.setObjectName("pushButton_8")
        self.todayButton.clicked.connect(self.showTrends)

        # ------------------------------
        # SECTION: Calendar button
        # ------------------------------
        self.Calander = QtWidgets.QFrame(self.centralwidget)
        self.Calander.setGeometry(QtCore.QRect(70, 190, 121, 111))
        self.Calander.setStyleSheet("QFrame {\n"
                                    "background-color: rgb(232, 228, 214);\n"
                                    "border: 2px solid black;\n"
                                    "border-radius: 10px;\n"
                                    "}")
        self.Calander.setObjectName("Calander")

        self.calendarButton = QtWidgets.QPushButton(self.Calander)
        self.calendarButton.setGeometry(QtCore.QRect(20, 20, 81, 71))
        self.calendarButton.setText("")
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap("bilder/Calendar.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.calendarButton.setIcon(icon7)
        self.calendarButton.setIconSize(QtCore.QSize(120, 50))
        self.calendarButton.setFlat(True)
        self.calendarButton.setObjectName("pushButton")
        self.calendarButton.clicked.connect(self.openCalendar)

        # ------------------------------
        # SECTION: Set the central widget
        # ------------------------------
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    # ------------------------------
    # SECTION: Set up translatable text
    # ------------------------------
    def retranslateUi(self, MainWindow):
        """ Sets the window title and any translatable text. """
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Expressly"))

    # ------------------------------
    # SECTION: Open the statistics window
    # ------------------------------
    def showTrends(self):
        """ Opens the statistics window when the 'Today' button is clicked. """
        try:
            self.trendWindow = TrendOverviewWindow()
            trendData = getTrendDataFromFirebase()  
            self.trendWindow.updateTrends(trendData)
            self.trendWindow.show()
        except Exception as e:
            print(f"Error opening statistics window: {e}")

    # ------------------------------
    # SECTION: Open the calendar
    # ------------------------------
    def openCalendar(self):
        """ Opens the calendar window """
        self.calendarWindow = QtWidgets.QMainWindow()
        self.ui = Ui_Form()
        self.ui.setupUi(self.calendarWindow)
        self.calendarWindow.show()


<<<<<<< HEAD
# Authenticate as an anonymous user
def getUserId():    
    # Initialize QSettings
    settings = QSettings("Expressly", "Expressly")

    savedUid = settings.value("uid")
    #Check if user id exists
    if savedUid:
        print("✅ User id found")
        print(settings.fileName())
        return savedUid
        
    else:
        #Create new user id and save it in settings
        print("No existing user id found, creating new user id")
        APIKEY = "AIzaSyAT-jTtpqOeqJntmwcyFEUBb7YRQmA46rU"
        url = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={APIKEY}"
        response = requests.post(url, json={})

        #Check if the response is successful
        if response.status_code == 200:
            token = response.json()["idToken"]
            print("✅ Anonymous user signed in successfully.")
            settings.setValue("uid", token)
            return token
        else:
            print("❌ Failed to authenticate:", response.json())
            return None

# Get user id
userId = getUserId()


# Entry point, starts the program
=======
# ------------------------------
# SECTION: Run the program
# ------------------------------
>>>>>>> jessie
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = uiMainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

