import os
import sys
import re
from datetime import datetime
from PyQt5 import QtCore, QtGui, QtWidgets
from pyqtgraph import PlotWidget
from PyQt5.QtCore import QSettings

# Firebase imports
import firebase_admin
from firebase_admin import credentials, firestore

# Debugging
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

# Maps kaomoji to mood strings
KAOMOJI_MOOD_MAP = {
    "(╯︵╰,)": "sad",
    "ヽ(ー_ー )ノ": "neutral",
    "ヽ(◕‿◕｡)ノ": "very happy",
    "(◕‿◕) ": "happy",
    "(－_－) zzZ ": "tired",
    "ヽ( д´*)ノ": "angry",
}

# Maps mood strings to numeric values (0-10)
MOOD_MAP = {
    "veryhappy": 10,
    "happy": 8,
    "neutral": 6,
    "sad": 4,
    "tired": 2,
    "angry": 0
}

# ------------------------------
# SECTION: Parsing Activity Data
# ------------------------------

def parseActivityLine(line):
    """
    Parses a line like:
      "School (Energy: 7/10) ヽ(ー_ー )ノ"
    Extracts:
      - Energy level (integer)
      - Mood (as a string)
    If the kaomoji is not recognized, defaults to "angry".
    """
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
    """
    Retrieves saved mood and energy statistics from Firebase.
    """
    if not firebase_admin._apps:
        cred = credentials.Certificate("serviceAccountKey.json")
        firebase_admin.initialize_app(cred)
    db = firestore.client()

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

        validLevels = [0, 2, 4, 6, 8, 10]
        bestMatch = min(validLevels, key=lambda x: abs(x - avgMoodNum))
        moodStr = next((k for k, v in MOOD_MAP.items() if v == bestMatch), "angry")

        dataList.append({"date": dateStr, "energy": avgEnergy, "mood": moodStr})

    dataList.sort(key=lambda x: x["date"])
    return dataList

# ------------------------------
# SECTION: Trend Overview Window
# ------------------------------

class TrendOverviewWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(TrendOverviewWindow, self).__init__(parent)
        self.setWindowTitle("Trend Overview")
        self.setFixedSize(800, 600)
        self.setStyleSheet(f"background-color: {CALENDAR_BG_COLOR};")

        # Create graph widget
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

        # Custom Y-axis labels for moods
        yTicks = [(v, f"{v}\n{k.capitalize()}") for k, v in MOOD_MAP.items()]
        leftAxis = self.plotItem.getAxis('left')
        leftAxis.setTicks([yTicks])

        # Set the title at the top center of the graph
        self.plotItem.setTitle("<h2>Trend Overview</h2>", color="black", size="14pt")

    def updateTrends(self, dataList):
        """
        Updates the trend graph with Firebase data.
        Ensures only valid date entries are processed.
        """
        self.plotItem.clear()

        if not dataList:
            print("No data found.")
            return

        # Filter out invalid document IDs that are not in the expected YYYY-MM-DD format
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

        # Retrieve energy and mood values
        energyValues = [item["energy"] for item in validData]
        moodValues = [MOOD_MAP.get(item["mood"].lower(), 0) for item in validData]

        # Create pens for the lines
        energyPen = QtGui.QPen(QtGui.QColor("#8caa9a"))  # Green for energy
        energyPen.setWidth(3)
        energyPen.setCosmetic(True)

        moodPen = QtGui.QPen(QtGui.QColor(139, 69, 19))  # Brown for mood
        moodPen.setWidth(3)
        moodPen.setCosmetic(True)

        # Plot both lines using the same X-axis values
        self.plotItem.plot(xValues, energyValues, pen=energyPen, name="Energy")
        self.plotItem.plot(xValues, moodValues, pen=moodPen, name="Mood")

        # Set custom axis labels
        bottomAxis = self.plotItem.getAxis('bottom')
        customXTicks = [(i, formattedDates[i] + " ") for i in range(len(formattedDates))]
        bottomAxis.setHeight(40)  # Adjust spacing below labels
        bottomAxis.setTicks([customXTicks])

        # Ensure smooth scrolling instead of zooming
        self.plotItem.setXRange(0, len(formattedDates) - 1, padding=0)
        self.plotItem.getViewBox().setLimits(xMin=0, xMax=len(formattedDates) - 1)
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
