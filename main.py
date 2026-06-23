from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QWidget, QGroupBox, QGridLayout, QComboBox, QDoubleSpinBox, QPushButton, QVBoxLayout, QListWidget, QMessageBox, QInputDialog
import sys
import json
import os
HISTORY_FILE = "history.json" 

class UnitConverter(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Unit Converter")
        self.resize(720, 400)

        centralWidget = QWidget()
        self.setCentralWidget(centralWidget)
        centralWidgetVBoxLayout = QVBoxLayout()

        conversionBox = QGroupBox()
        conversionGrid = QGridLayout()

        self.amount = QDoubleSpinBox()

        self.firstUnit = QComboBox()
        self.firstUnit.addItems(["Inch", "Foot", "Yard", "Mile", "Millimeter", "Centimeter", "Decimeter", "Meter", "Kilometer"])

        self.secondUnit = QComboBox()
        self.secondUnit.addItems(["Inch", "Foot", "Yard", "Mile", "Millimeter", "Centimeter", "Decimeter", "Meter", "Kilometer"])

        self.conversionMeterBasis = {
            "Inch": 0.0254,
            "Foot": 0.3048,
            "Yard": 0.9144,
            "Mile": 1609.34,
            "Millimeter": 0.001,
            "Centimeter": 0.01,
            "Decimeter": 0.1,
            "Meter": 1.0,
            "Kilometer": 1000.0 
        }

        conversionGrid.addWidget(QLabel("Amount: "), 0, 0)
        conversionGrid.addWidget(self.amount, 1, 0)

        conversionGrid.addWidget(QLabel("From: "), 0, 1) # Figure out how to add in the units later
        conversionGrid.addWidget(self.firstUnit, 1, 1)

        conversionGrid.addWidget(QLabel("To: "), 0, 2)
        conversionGrid.addWidget(self.secondUnit, 1, 2)

        conversionBox.setLayout(conversionGrid)


        buttonBox = QGroupBox()
        buttonGrid = QGridLayout()

        self.convertButton = QPushButton("Convert")
        self.clearButton = QPushButton("Clear History") #Unique thingy for later. Clear out history
        self.renameButton = QPushButton("Rename Window")

        buttonGrid.addWidget(self.convertButton, 0, 0)
        buttonGrid.addWidget(self.clearButton, 0, 1)
        buttonGrid.addWidget(self.renameButton, 0, 2)

        buttonBox.setLayout(buttonGrid)


        resultBox = QGroupBox()
        resultVBoxLayout = QVBoxLayout()
        
        self.resultLabel = QLabel("Conversion: ")
        self.statsLabel = QLabel("You have made 0 conversions")

        resultVBoxLayout.addWidget(self.resultLabel)
        resultVBoxLayout.addWidget(self.statsLabel)

        resultBox.setLayout(resultVBoxLayout)

        historyBox = QGroupBox()
        historyVBoxLayout = QVBoxLayout()

        self.historyList = QListWidget()

        historyVBoxLayout.addWidget(self.historyList)

        historyBox.setLayout(historyVBoxLayout)

        centralWidgetVBoxLayout.addWidget(conversionBox)
        centralWidgetVBoxLayout.addWidget(buttonBox)
        centralWidgetVBoxLayout.addWidget(resultBox)
        centralWidgetVBoxLayout.addWidget(historyBox)

        centralWidget.setLayout(centralWidgetVBoxLayout)

        self.convertButton.clicked.connect(self.convert)
        self.clearButton.clicked.connect(self.clearHistory)
        self.renameButton.clicked.connect(self.renameWindow)
        
        self.amount.valueChanged.connect(self.convertNoHistory)

        histories = self.loadHistory()
        self.totalConversions = histories["totalConversions"]

        for history in histories["history"]:
            self.historyList.addItem(history)
        
        self.statsLabel.setText(f"You have made {self.totalConversions} conversions")

        self.setStyleSheet("""
        QMainWindow {
            background-color: #E7E7E7;
        }

        QListWidget, QComboBox, QDoubleSpinBox{
            background-color: #F3F3F3;
            padding: 5px;
        }

        QPushButton{
            background-color: #F0F0F0;
            border-radius: 5px;
            padding: 5px;
        }

        QPushButton:hover{
            background-color: #EBEBEB;
        }
                           
        QGroupBox{
            background-color: #F8F8F8;
            padding 10px;
        }
        """)

    def loadHistory(self):
        if not os.path.exists(HISTORY_FILE):
            return {
                "history": [],
                "totalConversions": 0
            }
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    
    def saveHistory(self, history, totalConversions):
        histories = {
            "history": history,
            "totalConversions": totalConversions
        }
        with open(HISTORY_FILE, "w") as f:
            json.dump(histories, f, indent=2)
    
    def saveCurrentHistory(self):
        history = []
        for i in range(self.historyList.count()):
            history.append(self.historyList.item(i).text())
        
        self.saveHistory(history, self.totalConversions)

    def convert(self):
        convert1 = self.amount.value()

        startUnit = self.firstUnit.currentText()
        endUnit = self.secondUnit.currentText()

        result = (convert1*self.conversionMeterBasis[startUnit]) / self.conversionMeterBasis[endUnit]

        resultText = f"{convert1:.6f} {startUnit} = {result:.6f} {endUnit}"

        self.resultLabel.setText(resultText)

        self.historyList.addItem(resultText)

        self.totalConversions += 1

        self.statsLabel.setText(f"You have made {self.totalConversions} conversions")
        
        self.saveCurrentHistory()
    
    def convertNoHistory(self, convert1):

        startUnit = self.firstUnit.currentText()
        endUnit = self.secondUnit.currentText()

        result = (convert1*self.conversionMeterBasis[startUnit]) / self.conversionMeterBasis[endUnit]

        resultText = f"{convert1:.6f} {startUnit} = {result:.6f} {endUnit}"

        self.resultLabel.setText(resultText)

    def clearHistory(self):
        reply = QMessageBox.question(self, "Clear History", "Are you sure you want to clear your conversion history?", QMessageBox.Yes | QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.historyList.clear()

            self.totalConversions = 0

            self.statsLabel.setText("You have made 0 conversions")
            self.saveCurrentHistory()

    def renameWindow(self):
        newTitle, ok = QInputDialog.getText(self, "Rename Window", "Enter a new name: ")

        if ok and newTitle:
            self.setWindowTitle(newTitle)

app = QApplication(sys.argv)
window = UnitConverter()
window.show()
app.exec()