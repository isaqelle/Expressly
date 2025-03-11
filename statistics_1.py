import os
import sys
import re
from datetime import datetime
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QSettings
from pyqtgraph import BarGraphItem, LegendItem, PlotWidget
import firebase_admin
from firebase_admin import credentials, firestore

# ------------------------------
# SECTION: Debugging & Setup
# ------------------------------
print("Current working directory:", os.getcwd())
print("Checking if serviceAccountKey.json exists:", os.path.isfile("serviceAccountKey.json"))

# ------------------------------
# SECTION: User ID
# Finds user ID from the settings file
# ------------------------------
settings = QSettings("\HKEY_CURRENT_USER\Software\Expressly\Expressly", QSettings.NativeFormat)
UserId = settings.value("uid")

# ------------------------------
# SECTION: Global Constants and Mood Mapping
# ------------------------------
CALENDAR_BG_COLOR = "#e8e4d6"  # Light background color for the calendar

# Kaomoji-to-mood mapping
KAOMOJI_MOOD_MAP = {
    "(╯︵╰,)": "sad",
    "ヽ(ー_ー )ノ": "neutral",
    "ヽ(◕‿◕｡)ノ": "veryHappy",
    "(◕‿◕)": "happy",
    "(－_－) zzZ": "tired",
    "ヽ( `д´*)ノ": "angry",
}

# Mood-to-numeric mapping
MOOD_MAP = {
    "veryhappy": 10,
    "happy": 8,
    "neutral": 6,
    "sad": 4,
    "tired": 2,
    "angry": 0
}

# ------------------------------
# SECTION: Data Parsing
# ------------------------------
def parseActivityLine(line):
    # Parses an activity line and extracts energy level and mood.
    energyVal = 0
    moodStr = "angry"

    pattern = r"^(.+?) \(Energy:\s*(\d+)/10\)\s*(.*)$"
    match = re.match(pattern, line)

    if match:
        energyVal = int(match.group(2))
        kaomoji = match.group(3).strip()
        moodStr = KAOMOJI_MOOD_MAP.get(kaomoji, "angry")

    return energyVal, moodStr

# ------------------------------
# SECTION: Firebase Retrieval
# ------------------------------
def getTrendDataFromFirebase():
    # Retrieves saved mood and energy statistics from Firebase.
    if not firebase_admin._apps:
        cred = credentials.Certificate("serviceAccountKey.json")
        firebase_admin.initialize_app(cred)
    db = firestore.client()

    # Get the current week's Monday and Sunday
    dataList = []  
    docs = db.collection("users").document(UserId).collection("calendar_entries").stream()

    for doc in docs:
        dateStr = doc.id  # Document ID as date (e.g., "2025-03-02")
        docData = doc.to_dict()
        activitiesText = docData.get("activities", "")
        lines = activitiesText.splitlines()

        energies = []
        moodNumbers = []

        for line in lines:
            energyVal, moodKao = parseActivityLine(line)
            energies.append(energyVal)
            numericMood = MOOD_MAP.get(moodKao.lower(), 0)
            moodNumbers.append(numericMood)

        avgEnergy = sum(energies) / len(energies) if energies else 0
        avgMoodNum = sum(moodNumbers) / len(moodNumbers) if moodNumbers else 0

        moodNum = round(avgMoodNum)

        dataList.append({"date": dateStr, "energy": avgEnergy, "mood": moodNum})  # moodNum istället för moodStr

    dataList.sort(key=lambda x: x["date"])
    return dataList

# ------------------------------
# SECTION: Trend Overview Window
# ------------------------------
class TrendOverviewWindow(QtWidgets.QMainWindow):
    # Graphical window displaying energy and mood trends.
    def __init__(self, parent=None):
        super(TrendOverviewWindow, self).__init__(parent)
        self.setWindowTitle("Trend Overview")
        self.setFixedSize(800, 600)
        self.setStyleSheet(f"background-color: {CALENDAR_BG_COLOR};")

        self.graphWidget = PlotWidget(self)
        self.graphWidget.setGeometry(QtCore.QRect(10, 10, 780, 580))
        self.graphWidget.setBackground(CALENDAR_BG_COLOR)

        self.plotItem = self.graphWidget.getPlotItem()
        self.plotItem.clear()
        self.plotItem.showGrid(x=True, y=True, alpha=0.3)
        self.plotItem.setMouseEnabled(x=True, y=False)

        font = QtGui.QFont()
        font.setPointSize(12)
        self.plotItem.setLabel('left', 'Energy & Mood')
        self.plotItem.setLabel('bottom', 'Date')
        self.plotItem.addLegend()

        # Custom Y-axis labels
        yTicks = [(v, f"{v}\n{k.capitalize()}") for k, v in MOOD_MAP.items()]
        leftAxis = self.plotItem.getAxis('left')
        leftAxis.setTicks([yTicks])

        # Set the title at the top center of the graph
        self.plotItem.setTitle("<h2>Trend Overview</h2>", color="black", size="14pt")

    def updateTrends(self, dataList):
        # Updates the trend graph with Firebase data.
        self.plotItem.clear()
        if not dataList:
            print("No data found.")
            return

        # Validate and format dates
        validData = []
        for item in dataList:
            try:
                datetime.strptime(item["date"], "%Y-%m-%d")  # Validate date format
                validData.append(item)
            except ValueError:
                print(f"Skipping invalid document: {item['date']}")  # Debugging

        if not validData:
            print("No valid dates found in Firebase.")
            return

        # Extract and format dates
        dateStrings = sorted([item["date"] for item in validData])
        formattedDates = [datetime.strptime(date, "%Y-%m-%d").strftime("%d/%m") for date in dateStrings]

        xValues = list(range(len(formattedDates)))

        # Extracts values
        energyValues = [item["energy"] for item in validData]
        moodValues = [item["mood"] for item in validData]  # Behåller hela skalan 0-10

        # Create bars
        energyBars = BarGraphItem(x=xValues, height=energyValues, width=0.3, brush=QtGui.QColor("#8caa9a"))  # Green
        moodBars = BarGraphItem(x=[x + 0.35 for x in xValues], height=moodValues, width=0.3, brush=QtGui.QColor("#aa7d51"))  # Brown

        # Plot both lines using the same X-axis values
        self.plotItem.addItem(energyBars)
        self.plotItem.addItem(moodBars)

        # Custom X-axis labels
        bottomAxis = self.plotItem.getAxis('bottom')
        customXTicks = [(i, formattedDates[i] + " ") for i in range(len(formattedDates))]
        bottomAxis.setHeight(40)  # Adjust spacing below labels
        bottomAxis.setTicks([customXTicks])

        # Set fixed X-axis range to maintain consistent scrolling behavior
        self.plotItem.setXRange(-1, len(formattedDates), padding=0.1)
        self.plotItem.getViewBox().setLimits(xMin=-0.5, xMax=len(formattedDates) - 0.5)

        # Add legend for energy and mood levels
        self.legend = LegendItem((100, 60), offset=(-10, 10))  # (width, height), (x-offset, y-offset)
        self.legend.setParentItem(self.plotItem)
        self.legend.addItem(energyBars, "Energy Level")
        self.legend.addItem(moodBars, "Mood Level")

# ------------------------------
# SECTION: Main Function
# ------------------------------
def main():
    app = QtWidgets.QApplication(sys.argv)
    window = TrendOverviewWindow()
    trendData = getTrendDataFromFirebase()
    window.updateTrends(trendData)
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
