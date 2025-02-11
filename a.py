# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindowtry1.ui'
#
# Created by: PyQt5 UI code generator 5.15.11
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(500, 400)
        MainWindow.setMaximumSize(QtCore.QSize(500, 400))
        MainWindow.setStyleSheet("QMainWindow {\n"
"    background-color: rgb(185, 217, 186);\n"
"}\n"
"")
        MainWindow.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setStyleSheet("")
        self.centralwidget.setObjectName("centralwidget")
        self.Emojitabell = QtWidgets.QFrame(self.centralwidget)
        self.Emojitabell.setGeometry(QtCore.QRect(280, 60, 161, 241))
        self.Emojitabell.setTabletTracking(False)
        self.Emojitabell.setToolTipDuration(-2)
        self.Emojitabell.setAutoFillBackground(False)
        self.Emojitabell.setStyleSheet("QFrame {\n"
"background-color: rgb(232, 228, 214);\n"
"border: 2px solid black;\n"
"border-radius: 10px; \n"
"}\n"
"")
        self.Emojitabell.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.Emojitabell.setFrameShadow(QtWidgets.QFrame.Raised)
        self.Emojitabell.setObjectName("Emojitabell")
        self.gridLayout = QtWidgets.QGridLayout(self.Emojitabell)
        self.gridLayout.setObjectName("gridLayout")
        self.VeryHappy = QtWidgets.QPushButton(self.Emojitabell)
        self.VeryHappy.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("Agile-Demo/bilder/grinning-face-with-big-eyes_1f603.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.VeryHappy.setIcon(icon)
        self.VeryHappy.setIconSize(QtCore.QSize(55, 55))
        self.VeryHappy.setAutoRepeat(False)
        self.VeryHappy.setAutoRepeatDelay(297)
        self.VeryHappy.setFlat(True)
        self.VeryHappy.setObjectName("VeryHappy")
        self.gridLayout.addWidget(self.VeryHappy, 0, 0, 1, 1)
        self.Happy = QtWidgets.QPushButton(self.Emojitabell)
        self.Happy.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("Agile-Demo/bilder/slightly-smiling-face_1f642.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Happy.setIcon(icon1)
        self.Happy.setIconSize(QtCore.QSize(55, 55))
        self.Happy.setAutoRepeat(False)
        self.Happy.setAutoRepeatDelay(299)
        self.Happy.setFlat(True)
        self.Happy.setObjectName("Happy")
        self.gridLayout.addWidget(self.Happy, 0, 1, 1, 1)
        self.Sad = QtWidgets.QPushButton(self.Emojitabell)
        self.Sad.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("Agile-Demo/bilder/crying-face_1f622.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Sad.setIcon(icon2)
        self.Sad.setIconSize(QtCore.QSize(55, 55))
        self.Sad.setAutoRepeat(False)
        self.Sad.setAutoRepeatDelay(298)
        self.Sad.setFlat(True)
        self.Sad.setObjectName("Sad")
        self.gridLayout.addWidget(self.Sad, 1, 0, 1, 1)
        self.neutral = QtWidgets.QPushButton(self.Emojitabell)
        self.neutral.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("Agile-Demo/bilder/neutral-face_1f610.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.neutral.setIcon(icon3)
        self.neutral.setIconSize(QtCore.QSize(55, 55))
        self.neutral.setAutoRepeat(False)
        self.neutral.setAutoRepeatDelay(299)
        self.neutral.setFlat(True)
        self.neutral.setObjectName("neutral")
        self.gridLayout.addWidget(self.neutral, 1, 1, 1, 1)
        self.Angry = QtWidgets.QPushButton(self.Emojitabell)
        self.Angry.setText("")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("Agile-Demo/bilder/pouting-face_1f621.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Angry.setIcon(icon4)
        self.Angry.setIconSize(QtCore.QSize(55, 55))
        self.Angry.setAutoRepeat(False)
        self.Angry.setAutoRepeatDelay(299)
        self.Angry.setFlat(True)
        self.Angry.setObjectName("Angry")
        self.gridLayout.addWidget(self.Angry, 2, 0, 1, 1)
        self.tired = QtWidgets.QPushButton(self.Emojitabell)
        self.tired.setText("")
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("bilder/sleeping-face_1f634.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tired.setIcon(icon5)
        self.tired.setIconSize(QtCore.QSize(55, 55))
        self.tired.setAutoRepeat(False)
        self.tired.setAutoRepeatDelay(299)
        self.tired.setFlat(True)
        self.tired.setObjectName("tired")
        self.gridLayout.addWidget(self.tired, 2, 1, 1, 1)
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
        self.pushButton_8 = QtWidgets.QPushButton(self.TodaysCalander)
        self.pushButton_8.setGeometry(QtCore.QRect(20, 20, 81, 71))
        self.pushButton_8.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.pushButton_8.setText("")
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap("Agile-Demo/bilder/Today.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_8.setIcon(icon6)
        self.pushButton_8.setIconSize(QtCore.QSize(125, 50))
        self.pushButton_8.setFlat(True)
        self.pushButton_8.setObjectName("pushButton_8")
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
        self.pushButton = QtWidgets.QPushButton(self.Calander)
        self.pushButton.setGeometry(QtCore.QRect(20, 20, 81, 71))
        self.pushButton.setText("")
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap("Agile-Demo/bilder/Calendar.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton.setIcon(icon7)
        self.pushButton.setIconSize(QtCore.QSize(120, 50))
        self.pushButton.setFlat(True)
        self.pushButton.setObjectName("pushButton")
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

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
