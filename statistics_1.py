import os
import sys
import re
from PyQt5 import QtCore, QtGui, QtWidgets
from pyqtgraph import PlotWidget

# Some debugging code, checking the current working directory and verifying that "serviceAccountKey.json" exists
print("Current working directory:", os.getcwd())
print("Checking if serviceAccountKey.json exists:", os.path.isfile("serviceAccountKey.json"))

# ------------------------------
# SECTION: Global Constants and Mood Mapping
# ------------------------------
CALENDAR_BG_COLOR = "#e8e4d6"  # Same light background as the calendar

# Maps kaomoji to mood strings
KAOMOJI_MOOD_MAP = {
    "(╯︵╰,)": "sad",
    "ヽ(ー_ー )ノ": "neutral",
    "ヽ(◕‿◕｡)ノ": "very happy",
    "(◕‿◕) ": "happy",
    "(－_－) zzZ ": "tired",
    "ヽ( д´*)ノ": "angry",
    # Add more kaomojis here as needed
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
# SECTION: Parsing and Firebase Retrieval
# ------------------------------

def parseActivityLine(line):
    """
    Parses a line like:
      "Fore (Energy: 5/10) (╯︵╰,)"
    or
      "School (Energy: 7/10) ヽ(ー_ー )ノ"
    Returns a tuple (energy, moodString).
    If the kaomoji is not recognized, defaults to "angry".
    """
    energyVal = 0
    moodStr = "angry"

    # Regex pattern explanation:
    # ^(.+?)             -> group(1): activity name (non-greedy)
    #  \(Energy:\s*(\d+)/10\) -> group(2): the energy integer
    #  \s*(.*)$          -> group(3): whatever remains (kaomoji)
    pattern = r"^(.+?) \(Energy:\s*(\d+)/10\)\s*(.*)$"
    match = re.match(pattern, line)
    if match:
        energyVal = int(match.group(2))
        kaomoji = match.group(3).strip()
        # Convert kaomoji to a mood string
        moodStr = KAOMOJI_MOOD_MAP.get(kaomoji, "angry")

    return energyVal, moodStr

def getTrendDataFromFirebase():
    """
    Reads from the 'calendar_entries' collection in Firestore.
    Each document:
      - Document ID is a date (e.g. "2025-03-02")
      - 'activities' is a multiline string with lines like:
            "Fore (Energy: 5/10) (╯︵╰,)"
            "School (Energy: 7/10) ヽ(ー_ー )ノ"
    Returns a list of dicts: [{"date": <docID>, "energy": avgEnergy, "mood": avgMoodStr}, ...]
    sorted by date.
    """
    import firebase_admin
    from firebase_admin import credentials, firestore

    # Initialize Firebase if not already done
    if not firebase_admin._apps:
        cred = credentials.Certificate("serviceAccountKey.json")
        firebase_admin.initialize_app(cred)
    db = firestore.client()

    dataList = []
    docs = db.collection("calendar_entries").stream()

    for doc in docs:
        dateStr = doc.id  # e.g. "2025-03-02"
        docData = doc.to_dict()
        activitiesText = docData.get("activities", "")
        lines = activitiesText.splitlines()

        energies = []
        moodNumbers = []

        for line in lines:
            energyVal, moodKao = parseActivityLine(line)
            energies.append(energyVal)
            # Convert moodKao to a numeric mood
            numericMood = MOOD_MAP.get(moodKao.lower(), 0)
            moodNumbers.append(numericMood)

        # Compute daily average energy
        if energies:
            avgEnergy = sum(energies) / len(energies)
        else:
            avgEnergy = 0

        # Compute daily average mood (numeric)
        if moodNumbers:
            avgMoodNum = sum(moodNumbers) / len(moodNumbers)
            # Round to the closest valid mood (0,2,4,6,8,10)
            validLevels = [0, 2, 4, 6, 8, 10]
            bestMatch = min(validLevels, key=lambda x: abs(x - avgMoodNum))
            # Convert numeric mood back to a mood string
            moodStr = next((k for k, v in MOOD_MAP.items() if v == bestMatch), "angry")
        else:
            moodStr = "angry"

        dataList.append({
            "date": dateStr,
            "energy": avgEnergy,
            "mood": moodStr
        })

    # Sort by date if doc IDs are in ISO format
    dataList.sort(key=lambda x: x["date"])
    return dataList

# ------------------------------
# SECTION: Trend Overview Window
# Creates a window (800x600) to display energy and mood trends using pyqtgraph
# ------------------------------
class TrendOverviewWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(TrendOverviewWindow, self).__init__(parent)
        self.setWindowTitle("Trend Overview")
        self.setFixedSize(800, 600)

        # Set window background color
        self.setStyleSheet(f"background-color: {CALENDAR_BG_COLOR};")

        # Create a QFrame with the same style as the calendar (background, black border, rounded corners)
        self.frame = QtWidgets.QFrame(self)
        self.frame.setGeometry(QtCore.QRect(0, 0, 800, 600))
        self.frame.setStyleSheet(f"""
            QFrame {{
                background-color: {CALENDAR_BG_COLOR};
                border: 2px solid black;
                border-radius: 10px;
            }}
        """)

        # Create a PlotWidget inside the frame
        self.graphWidget = PlotWidget(self.frame)
        self.graphWidget.setGeometry(QtCore.QRect(10, 10, 780, 580))
        self.graphWidget.setBackground(CALENDAR_BG_COLOR)

        # Get the PlotItem to adjust axes, grid, etc.
        self.plotItem = self.graphWidget.getPlotItem()
        self.plotItem.clear()

        # Show grid for a typical line chart appearance
        self.plotItem.showGrid(x=True, y=True, alpha=0.3)
        
        # Display axes
        self.plotItem.showAxis('bottom')
        self.plotItem.showAxis('left')

        # Set labels for the axes
        self.plotItem.setLabel('left', 'Energy')
        self.plotItem.setLabel('bottom', 'X-Axis')

        # Lock axes range to 0-10
        self.plotItem.setXRange(0, 10)
        self.plotItem.setYRange(0, 10)

        # Add a legend to differentiate the lines
        self.plotItem.addLegend()

        # ------------------------------
        # SECTION: Custom X-Axis Ticks
        # Set custom tick labels on the bottom axis
        # ------------------------------
        customTicks = [
            (0, "angry"),
            (2, "tired"),
            (4, "sad"),
            (6, "neutral"),
            (8, "happy"),
            (10, "veryhappy")
        ]
        bottomAxis = self.plotItem.getAxis('bottom')
        bottomAxis.setTicks([customTicks])

    # ------------------------------
    # SECTION: Update Trends Function
    # Updates the trend graph with new energy and mood data.
    # dataList is expected to be a list of dictionaries, e.g.:
    # [
    #   {"energy": 7, "mood": "happy"},
    #   {"energy": 5, "mood": "sad"},
    #   ...
    # ]
    # ------------------------------
    def updateTrends(self, dataList):
        self.plotItem.clear()

        n = len(dataList)
        if n < 1:
            return  # Nothing to plot

        # Evenly distribute data points over the x-axis from 0 to 10
        if n > 1:
            xValues = [i * (10 / (n - 1)) for i in range(n)]
        else:
            xValues = [5]  # If only one point, place it in the middle

        # Extract energy values
        energyValues = [item["energy"] for item in dataList]

        # Map mood strings to numeric values using MOOD_MAP
        moodValues = []
        for item in dataList:
            moodStr = item.get("mood", "angry").lower()
            moodVal = MOOD_MAP.get(moodStr, 0)
            moodValues.append(moodVal)

        # Create a thin pen for the energy line (using the green color from the calendar header)
        energyPen = QtGui.QPen(QtGui.QColor("#8caa9a"))
        energyPen.setWidth(1)
        energyPen.setCosmetic(True)  # Ensures the pen width remains 1 pixel regardless of scaling

        # Create a thin pen for the mood line (brown), 1 pixel wide, cosmetic
        moodPen = QtGui.QPen(QtGui.QColor(139, 69, 19))
        moodPen.setWidth(1)
        moodPen.setCosmetic(True)

        # Plot the energy line without symbols or fill (clean, pencil-like stroke)
        self.plotItem.plot(
            xValues,
            energyValues,
            pen=energyPen,
            fillLevel=None,
            brush=None,
            name="Energy"
        )

        # Plot the mood line without symbols or fill
        self.plotItem.plot(
            xValues,
            moodValues,
            pen=moodPen,
            fillLevel=None,
            brush=None,
            name="Mood"
        )

# ------------------------------
# SECTION: Main Function
# Entry point for the trend overview module
# ------------------------------
def main():
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = TrendOverviewWindow()

    # Attempt to retrieve data from Firebase
    try:
        trendData = getTrendDataFromFirebase()
        if not trendData:
            print("No trend data found in Firebase, using fallback example data.")
            trendData = [
                {"date": "2025-02-20", "energy": 7, "mood": "happy"},
                {"date": "2025-02-21", "energy": 5, "mood": "sad"},
                {"date": "2025-02-22", "energy": 9, "mood": "veryhappy"},
                {"date": "2025-02-23", "energy": 2, "mood": "tired"},
                {"date": "2025-02-24", "energy": 4, "mood": "neutral"},
                {"date": "2025-02-25", "energy": 0, "mood": "angry"}
            ]
    except Exception as e:
        print(f"Error retrieving data from Firebase: {e}")
        print("Using fallback example data.")
        trendData = [
            {"date": "2025-02-20", "energy": 7, "mood": "happy"},
            {"date": "2025-02-21", "energy": 5, "mood": "sad"},
            {"date": "2025-02-22", "energy": 9, "mood": "veryhappy"},
            {"date": "2025-02-23", "energy": 2, "mood": "tired"},
            {"date": "2025-02-24", "energy": 4, "mood": "neutral"},
            {"date": "2025-02-25", "energy": 0, "mood": "angry"}
        ]

    # Update the trend graph with either Firebase or fallback data
    window.updateTrends(trendData)
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
