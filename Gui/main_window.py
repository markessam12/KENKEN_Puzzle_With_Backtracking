from pyQt5_style import *

import sys


class MainWindow(QMainWindow):
    sizeList = [
        "3 x 3",
        "4 x 4",
        "5 x 5",
        "6 x 6",
        "7 x 7",
        "8 x 8",
        "9 x 9"
    ]

    algorithmsList = [
        "Backtracking",
        "Backtracking with Forward Checking - FC",
        "Backtracking with Arc Consistency - AC"
    ]

    def __init__(self,toolName,toolIcon):
        super(MainWindow,self).__init__()
        # kenken solver icon & name
        self.setWindowTitle(toolName)
        self.setWindowIcon(QIcon(toolIcon))
        self.setGeometry(450, 150, 550, 400)

        # default values
        self.gameSize = None
        self.algorithmType = None
        self.error = False

        self.widget = Widget()
        self.mainLayout = Layout()
        self.startGameLayout()

        self.widget.setLayout(self.mainLayout)
        self.setCentralWidget(self.widget)
        # menu bar
        self.menuBar = QMenuBar(self)
        self.setMenuBar(self.menuBar)
        self.addFileMenu()
        self.addHelpMenu()


    def addFileMenu(self):

        self.fileMenu = self.menuBar.addMenu('File')

        self.kenkenGameRules = QAction('Game Rules', self)
        self.kenkenGameRules.setIcon(QIcon('Images/gameRulesIcon.png'))
        self.fileMenu.addAction(self.kenkenGameRules)
        self.kenkenGameRules.triggered.connect(self.gameRulesAction)

        self.exitItem = QAction('Exit', self)
        self.exitItem.setIcon(QIcon('Images/exit.png'))
        self.fileMenu.addAction(self.exitItem)
        self.exitItem.triggered.connect(self.exitItemAction)

    def addHelpMenu(self):
        self.helpMenu = self.menuBar.addMenu('Help')
        self.helpMenuItem = QAction('About', self)
        self.helpMenuItem.setIcon(QIcon("Images/help.png"))
        self.helpMenu.addAction(self.helpMenuItem)
        self.helpMenuItem.triggered.connect(self.helpItemAction)

    def createSizeButton(self):

        self.kenkenSizeButton = KenKenComboBox(placeHolder="Choose Game Size",listToFill=self.sizeList)
        self.kenkenSizeButton.setFixedSize(170, 30)
        self.kenkenSizeButton.move(100, 190)
        self.kenkenSizeButton.currentIndexChanged.connect(self.setGameSize)

        self.mainLayout.addWidget(self.kenkenSizeButton,0,Qt.AlignCenter)

    def createAlgorithmButton(self):

        self.algorithmChoiceButton = KenKenComboBox(placeHolder="Choose Algorithm", listToFill=self.algorithmsList)
        self.algorithmChoiceButton.setFixedSize(450, 30)
        self.algorithmChoiceButton.move(10, 190)
        self.algorithmChoiceButton.currentIndexChanged.connect(self.setGameAlgorithmType)

        self.mainLayout.addWidget(self.algorithmChoiceButton,0,Qt.AlignCenter)

    #Done
    def helpItemAction(self):
        self.helpWindow = QDialog(self)
        self.helpWindow.resize(500, 400)
        self.verticalLayout = QVBoxLayout(self.helpWindow)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.helpLabel = QPlainTextEdit(self.helpWindow)
        self.helpLabel.setObjectName("plainTextEdit")
        self.horizontalLayout.addWidget(self.helpLabel)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.helpWindow.setWindowIcon(QIcon('Images/foeAsu.png'))
        self.helpWindow.setGeometry(450, 100, 550, 550)
        self.helpWindow.setWindowTitle("About")

        aboutString = """Kenken puzzle solver made by ASU Engineers:
            
                 Name                                     StudentID
                 ------                                       ---------
            * Engy Khalaf Ahmed                     1700301
            * Mark Essam Fares                      1701086
            * Mark Mourad Gamil                     1701088
            * Eman Salah Shabaan                  1000024
            * Mohamed Tarek Mohamed          1701220
            * Mohamed AbdelAzeem                1701235
      
      
            
        Submitted to Prof. Dr. Manal Morad """

        self.helpLabel.appendPlainText(aboutString)
        self.helpLabel.setFont(QFont("Sanserif", 10))
        self.helpLabel.setStyleSheet("""QLabel {border: 1px solid #000;}""")
        self.helpLabel.setReadOnly(True)

        self.helpWindow.show()

    # Done
    def gameRulesAction(self):

        self.gameRulesWindow = QDialog(self)
        self.gameRulesWindow.resize(500, 400)
        self.vLayout = QVBoxLayout(self.gameRulesWindow)
        self.vLayout.setObjectName("verticalLayout")
        self.hLayout = QHBoxLayout()
        self.hLayout.setObjectName("horizontalLayout")
        self.gameRulesLabel = QPlainTextEdit(self.gameRulesWindow)
        self.gameRulesLabel.setObjectName("plainTextEdit")
        self.hLayout.addWidget(self.gameRulesLabel)
        self.vLayout.addLayout(self.hLayout)
        self.gameRulesWindow.setWindowIcon(QIcon('Images/gameRulesIcon.png'))
        self.gameRulesWindow.setGeometry(450, 100, 550, 550)
        self.gameRulesWindow.setWindowTitle("Kenken puzzle Rules")

        aboutString = """Kenken puzzle instructions:
        
        1.Fill in each square cell in the puzzle with a number between 1 and
            the size of the grid.
            
        2. Use each number exactly once in each row and each column.
        
        3. The numbers in each “Cage” (indicated by the single color) must combine —
            in any order — to produce the cage’s target number using the indicated
            math operation.
            
        4. No guessing is required. """

        self.gameRulesLabel.appendPlainText(aboutString)
        self.gameRulesLabel.setFont(QFont("Sanserif", 10))
        self.gameRulesLabel.setStyleSheet("""QLabel {border: 1px solid #000;}""")
        self.gameRulesLabel.setReadOnly(True)

        self.gameRulesWindow.show()

    def showPopUpMessage(self,title,msg):
        self.msg = QMessageBox()
        self.msg.setWindowTitle(str(title))
        self.msg.setText(str(msg))
        msgRun = self.msg.exec_()

    def showError(self,title,msg):
        msgError = QErrorMessage()
        msgError.setWindowTitle(title)
        msgError.setText(str(msg))

        # the main layout
    def startGameLayout(self):
        self.spaceLabel = Label("                            ")
        self.mainLayout.addWidget(self.spaceLabel)
        self.addSizeLabel()
        self.createSizeButton()
        self.mainLayout.addWidget(self.spaceLabel)
        self.addChooseAlgorithmLabel()
        self.createAlgorithmButton()
        self.mainLayout.addWidget(self.spaceLabel)
        self.addStartGameButton()
        self.mainLayout.addWidget(self.spaceLabel)

    def addSizeLabel(self):
        self.selectGameSizeLabel = Label(text = "Tap to select the game",fontSize= 18)
        self.sizeLabel = Label(text= "SIZE",fontSize= 24,setBold= True)

        # add them to layout
        self.mainLayout.addWidget(self.selectGameSizeLabel,0,Qt.AlignCenter)
        self.mainLayout.addWidget(self.sizeLabel,0,Qt.AlignCenter)


    def addChooseAlgorithmLabel(self):
        self.algorithmLabel = Label(text="Choose Algorithm:", fontSize=14)
        self.mainLayout.addWidget(self.algorithmLabel,0,Qt.AlignCenter)

    def addStartGameButton(self):
        self.startGameButton = PushButton(buttonText= "Start Game", picturePath="Images/startGame.png")
        self.startGameButton.setMinimumSize(400,60)
        self.startGameButton.setStyleSheet("border :2px solid black")
        self.mainLayout.addWidget(self.startGameButton,0,Qt.AlignCenter)

        self.startGameButton.clicked.connect(self.checkErrors)



    def checkErrors(self):

        if self.gameSize is None:
            self.showPopUpMessage(title= "Error message", msg = "You must choose game size")
            self.error = True

        elif self.algorithmType is None:
            self.showPopUpMessage(title= "Error message", msg = "Please Choose Algorithm first")
            self.error = True
        else:
            self.error = False

    def setGameSize(self):
        gameGrid = self.kenkenSizeButton.currentText()
        gameSize = gameGrid.split(" ")[0]
        self.gameSize = int(gameSize)

    def setGameAlgorithmType(self):

        algorithmType = self.algorithmChoiceButton.currentText()
        if algorithmType == "Backtracking":
            self.algorithmType = algorithmType
        elif algorithmType == "Backtracking with Forward Checking - FC":
            self.algorithmType = "ForwardChecking"
        elif algorithmType == "Backtracking with Arc Consistency - AC":
            self.algorithmType = "ArcConsistency"

    def getGameSize(self):
        return self.gameSize

    def getGameAlgorithmType(self):
        return self.algorithmType

    def exitItemAction(self):
        QApplication.quit()

    #TODO:


