from PyQt5 import QtCore, QtGui, QtWidgets
from audio import AudioPlayer
from calendar_1 import Ui_Form


# ------------------------------
# SECTION: MainWindow
# ------------------------------
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(500, 400)
        MainWindow.setMaximumSize(QtCore.QSize(500, 400))
        MainWindow.setStyleSheet("QMainWindow {\n"
"    background-color: rgb(185, 217, 186);\n"
"}\n"
"")
        
        self.audio_player = AudioPlayer()
        MainWindow.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setStyleSheet("")
        self.centralwidget.setObjectName("centralwidget")

# ------------------------------
# SECTION: Emoji Table
# ------------------------------

        self.emojiTable = QtWidgets.QFrame(self.centralwidget)
        self.emojiTable.setGeometry(QtCore.QRect(280, 60, 161, 241))
        self.emojiTable.setTabletTracking(False)
        self.emojiTable.setToolTipDuration(-2)
        self.emojiTable.setAutoFillBackground(False)
        self.emojiTable.setStyleSheet("QFrame {\n"
"background-color: rgb(232, 228, 214);\n"
"border: 2px solid black;\n"
"border-radius: 10px; \n"
"}\n"
"")
        self.emojiTable.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.emojiTable.setFrameShadow(QtWidgets.QFrame.Raised)
        self.emojiTable.setObjectName("emojiTable")
        self.gridLayout = QtWidgets.QGridLayout(self.emojiTable)
        self.gridLayout.setObjectName("gridLayout")

# ------------------------------
# SECTION: Emoji "Very happy"
# ------------------------------

        self.veryHappyEmoji = QtWidgets.QPushButton(self.emojiTable)
        self.veryHappyEmoji.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("bilder/grinning-face-with-big-eyes_1f603.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.veryHappyEmoji.setIcon(icon)
        self.veryHappyEmoji.setIconSize(QtCore.QSize(55, 55))
        self.veryHappyEmoji.setAutoRepeat(False)
        self.veryHappyEmoji.setAutoRepeatDelay(297)
        self.veryHappyEmoji.setFlat(True)
        self.veryHappyEmoji.setObjectName("veryHappyEmoji")
        self.gridLayout.addWidget(self.veryHappyEmoji, 0, 0, 1, 1)
        #import Very happyEmoji sound
        self.veryHappyEmoji.clicked.connect(lambda: self.audio_player.play_sound("audio_filer/VeryHappy.mp3"))
        
# ------------------------------
# SECTION: Emoji "Happy"
# ------------------------------

        self.happyEmoji = QtWidgets.QPushButton(self.emojiTable)
        self.happyEmoji.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("bilder/slightly-smiling-face_1f642.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.happyEmoji.setIcon(icon1)
        self.happyEmoji.setIconSize(QtCore.QSize(55, 55))
        self.happyEmoji.setAutoRepeat(False)
        self.happyEmoji.setAutoRepeatDelay(299)
        self.happyEmoji.setFlat(True)
        self.happyEmoji.setObjectName("happyEmoji")
        self.gridLayout.addWidget(self.happyEmoji, 0, 1, 1, 1)
        #import happyEmoji sound
        self.happyEmoji.clicked.connect(lambda: self.audio_player.play_sound("audio_filer/Happy.mp3"))

# ------------------------------
# SECTION: Emoji "Sad"
# ------------------------------

        self.sadEmoji = QtWidgets.QPushButton(self.emojiTable)
        self.sadEmoji.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("bilder/crying-face_1f622.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.sadEmoji.setIcon(icon2)
        self.sadEmoji.setIconSize(QtCore.QSize(55, 55))
        self.sadEmoji.setAutoRepeat(False)
        self.sadEmoji.setAutoRepeatDelay(298)
        self.sadEmoji.setFlat(True)
        self.sadEmoji.setObjectName("sadEmoji")
        self.gridLayout.addWidget(self.sadEmoji, 1, 0, 1, 1)
        #import sadEmoji sound
        self.sadEmoji.clicked.connect(lambda: self.audio_player.play_sound("audio_filer/Sad.mp3"))

# ------------------------------
# SECTION: Emoji "Neutral"
# ------------------------------

        self.neutralEmoji = QtWidgets.QPushButton(self.emojiTable)
        self.neutralEmoji.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("bilder/neutral-face_1f610.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.neutralEmoji.setIcon(icon3)
        self.neutralEmoji.setIconSize(QtCore.QSize(55, 55))
        self.neutralEmoji.setAutoRepeat(False)
        self.neutralEmoji.setAutoRepeatDelay(299)
        self.neutralEmoji.setFlat(True)
        self.neutralEmoji.setObjectName("neutral")
        self.gridLayout.addWidget(self.neutralEmoji, 1, 1, 1, 1)
        #import neutral sound
        self.neutralEmoji.clicked.connect(lambda: self.audio_player.play_sound("audio_filer/Neutral.mp3"))

# ------------------------------
# SECTION: Emoji "Angry"
# ------------------------------

        self.angryEmoji = QtWidgets.QPushButton(self.emojiTable)
        self.angryEmoji.setText("")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("bilder/pouting-face_1f621.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.angryEmoji.setIcon(icon4)
        self.angryEmoji.setIconSize(QtCore.QSize(55, 55))
        self.angryEmoji.setAutoRepeat(False)
        self.angryEmoji.setAutoRepeatDelay(299)
        self.angryEmoji.setFlat(True)
        self.angryEmoji.setObjectName("Angry")
        self.gridLayout.addWidget(self.angryEmoji, 2, 0, 1, 1)
        self.angryEmoji.clicked.connect(lambda: self.audio_player.play_sound("audio_filer/Angry.mp3"))

# ------------------------------
# SECTION: Emoji "Tired"
# ------------------------------

        self.tiredEmoji = QtWidgets.QPushButton(self.emojiTable)
        self.tiredEmoji.setText("")
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("bilder/sleeping-face_1f634.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tiredEmoji.setIcon(icon5)
        self.tiredEmoji.setIconSize(QtCore.QSize(55, 55))
        self.tiredEmoji.setAutoRepeat(False)
        self.tiredEmoji.setAutoRepeatDelay(299)
        self.tiredEmoji.setFlat(True)
        self.tiredEmoji.setObjectName("tired")
        self.gridLayout.addWidget(self.tiredEmoji, 2, 1, 1, 1)
        #import tired sound
        self.tiredEmoji.clicked.connect(lambda: self.audio_player.play_sound("audio_filer/Tired.mp3"))

# ------------------------------
# SECTION: Today
# ------------------------------

        self.TodaysCalander = QtWidgets.QFrame(self.centralwidget)
        self.TodaysCalander.setGeometry(QtCore.QRect(70, 60, 121, 111))
        self.TodaysCalander.setAutoFillBackground(False)
        self.TodaysCalander.setStyleSheet("QFrame {\n"
"background-color: rgb(232, 228, 214);\n"
"border: 2px solid black;\n"
"border-radius: 10px; \n"
"}\n"
"QFrame {\n"
"background-color: rgb(232, 228, 214);\n"
"border: 2px solid black;\n"
"border-radius: 10px; \n"
"}\n"
"")
        self.TodaysCalander.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.TodaysCalander.setFrameShadow(QtWidgets.QFrame.Raised)
        self.TodaysCalander.setObjectName("TodaysCalander")

# ------------------------------
# SECTION: "Today" button
# ------------------------------

        self.todayButton = QtWidgets.QPushButton(self.TodaysCalander)
        self.todayButton.setGeometry(QtCore.QRect(20, 20, 81, 71))
        self.todayButton.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.todayButton.setText("")
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap("bilder/Today.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.todayButton.setIcon(icon6)
        self.todayButton.setIconSize(QtCore.QSize(125, 50))
        self.todayButton.setFlat(True)
        self.todayButton.setObjectName("pushButton_8")

# ------------------------------
# SECTION: Calendar
# ------------------------------

        self.Calander = QtWidgets.QFrame(self.centralwidget)
        self.Calander.setGeometry(QtCore.QRect(70, 190, 121, 111))
        self.Calander.setAutoFillBackground(False)
        self.Calander.setStyleSheet("QFrame {\n"
"background-color: rgb(232, 228, 214);\n"
"border: 2px solid black;\n"
"border-radius: 10px; \n"
"}\n"
"QFrame {\n"
"background-color: rgb(232, 228, 214);\n"
"border: 2px solid black;\n"
"border-radius: 10px; \n"
"}\n"
"")
        self.Calander.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.Calander.setFrameShadow(QtWidgets.QFrame.Raised)
        self.Calander.setObjectName("Calander")

# ------------------------------
# SECTION: "Calendar" button
# ------------------------------

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
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 500, 18))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

# Set windowtitle on the main window
    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle("Expressly")
        

# Opens the calendar when clicked
    def openCalendar(self):
        self.calendar_window = QtWidgets.QMainWindow()
        self.ui = Ui_Form()  
        self.ui.setupUi(self.calendar_window)
        self.calendar_window.show()


# Entry point, starts the program
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
