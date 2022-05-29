from pyQt5_style import *
import time
import random


class KenkenGameWindow(QMainWindow):
    backWindow = pyqtSignal()

    # 40 colors
    colorsList = [
        '#fd9b6b','#bbff9e','#fcb295','#f4e409','#00a5cf','#f1489c','#ffb100','#56f1de',
        '#f3c178','#d5a473','#f2ca3a','#34bb9e','#63c132','#aaefdf','#f53cc9','#f79f79','#8c5383','#75f4f4','#d999d9',
        '#e3f09b','#aad922','#c1b2ab','#f5eccd','#e952de','#a7a2a9','#bacba9','#fa7921','#b9a44c','#c4a287',
        '#616283','#bfcc49','#a44a3f','#d4e09b','#b5f44a','#a1d538','#70ee9c','#07beb8','#8f3985','#62714f','#5bff5b'
    ]

    def __init__(self,toolName,toolIcon):
        super(KenkenGameWindow,self).__init__()
        # kenken solver icon & name
        self.setWindowTitle(toolName)
        self.setWindowIcon(QIcon(toolIcon))
        self.kenkenGameLayout = Layout()
        self.backButton = PushButton(buttonText=" Back", picturePath="Images/backButton.ico")
        self.checkButton = PushButton(buttonText=" Hint", picturePath="Images/checkButton.png")
        self.solveButton = PushButton(buttonText=" Solve", picturePath="Images/solve.ico")

        self.kenkenWidget = Widget()
        # ---window size depending on gameSize ---

        self.setGeometry(450, 150, 550, 400)

        self.setCentralWidget(self.kenkenWidget)

    def createKenkenGameLayout(self, gameSize = None,cagesDict = None):
        # try:
        if gameSize is not None:
            self.gameSize = gameSize

        temporaryLayout = Layout()
        self.temporaryGameBoard = GameBoardTable(gameSize= self.gameSize)


        # --- layout size depending on table game
        horizontalHeaderLength = self.temporaryGameBoard.horizontalHeader().length()
        verticalHeaderLength = self.temporaryGameBoard.verticalHeader().length()

        self.setGeometry(450,
                         150,
                         verticalHeaderLength + 70,
                         horizontalHeaderLength + 130)

        if cagesDict is not None:
            self.plotCagesOnGameBoard(cagesDict = cagesDict, gameBoardTable = self.temporaryGameBoard)
        temporaryLayout.addWidget(self.temporaryGameBoard, 0, Qt.AlignCenter)

        # ---temporaryButtons ---
        backButton = PushButton(buttonText=" Back", picturePath="Images/backButton.ico")
        checkButton = PushButton(buttonText=" Hint", picturePath="Images/checkButton.png")
        solveButton = PushButton(buttonText=" Solve", picturePath="Images/solve.ico")

        self.backButton = backButton
        self.checkButton = checkButton
        self.solveButton = solveButton

        temporaryLayout.addWidget(solveButton, 0, Qt.AlignCenter)
        tempHLayout = QHBoxLayout()
        tempHLayout.addWidget(backButton, 0, Qt.AlignLeft)
        tempHLayout.addWidget(checkButton, 0, Qt.AlignRight)

        temporaryLayout.addLayout(tempHLayout)
        print("Buttons added to layout")
        if (self.backButton.isChecked()):
            self.temporaryGameBoard.model().removeRows(0,self.temporaryGameBoard.rowCount())
            self.temporaryGameBoard.model().removeColumns(0,gameSize)
            print ("Table deleted")
        # --- set kenkenGameLayout to the temporary layout ---
        self.kenkenWidget.setLayout(temporaryLayout)

        print("layout setting correct")



    def plotCagesOnGameBoard(self,cagesDict,gameBoardTable):
        """ This function takes cagesDict, extract each cage cellsList to color it with colorsList in this class
        And takes gameBoardTable : which is temporary for every gameBoard and change with every time a new board
        is generated.
        each cellsList for a specific cage will be colored with a single color"""
        print ("cagesDict : ",cagesDict)
        for cageNumber in cagesDict:
            cageColor = self.colorsList[cageNumber]
            print(cageColor)
            cageString, cellsListOfCage = self.extractCageInfo(cageDict= cagesDict[cageNumber])
            self.setCageWidgets(cageColor = cageColor,
                                cellsList=cellsListOfCage,
                                cageString= cageString)

    # --- setters & getters ---
    def setGameSize(self,gameSize):
        self.gameSize = gameSize

    def connectBackWindow(self, function):
        self.backWindow.connect(function)

    def backButtonClicked(self):
        self.gameSize = None

        self.backWindow.emit()

    def extractCageInfo(self,cageDict):
        cageVal = cageDict['value']
        cageOp = cageDict['op']
        cageCellsList = cageDict['cells']

        if cageOp == "none":
            cageString = str(cageVal)
        else:
            cageString = str(cageVal) + cageOp

        print(cageString)
        return cageString,cageCellsList

    def setCageWidgets(self,cageColor,cellsList,cageString = " "):
        cellWidget = BoardCellWidget(color=cageColor,
                                    initialDomainSize=self.temporaryGameBoard.rowCount(),
                                    cageString=cageString)
        #1st cell
        # +1 because table has header row and col
        cageFirstCell = cellsList[0]
        rowIndex = cageFirstCell[0]
        colIndex = cageFirstCell[1]
        self.temporaryGameBoard.setCellWidget(rowIndex, colIndex, cellWidget)

        # writing the rest of cage
        for cellNumber in range(len(cellsList)):
            row = cellsList[cellNumber][0]  # index 0 means the first item in cell tuple , which means rowIndex
            col = cellsList[cellNumber][1]
            if (row, col) != cageFirstCell:
                #creating cell widget
                cellWidget = BoardCellWidget(color=cageColor,
                                             initialDomainSize=self.temporaryGameBoard.rowCount())
                #apply cell widget
                self.temporaryGameBoard.setCellWidget(row , col, cellWidget)

    def printFinalSolution(self,solution):
        for row in range(self.temporaryGameBoard.rowCount()):
            for col in range(self.temporaryGameBoard.columnCount()):
                self.temporaryGameBoard.cellWidget(row,col).solutionLineEdit.setText(str(solution[row][col]))
                #TODO: I want to animate displaying values in each cell. I want to make 1st value display and delay 1 sec,
                # then display the next value and so on.


    def checkSolutionButtonFunction(self,solution):
        """ referenceSolution of Solver"""

        isSolved =True
        for row in range(self.temporaryGameBoard.rowCount()):
            for col in range(self.temporaryGameBoard.columnCount()):
                userSolution = self.temporaryGameBoard.cellWidget(row, col).solutionLineEdit.text()
                referenceSolution = solution[row][col]
                if(int(userSolution) == referenceSolution ):
                    pass
                else:
                    isSolved = False

        return isSolved

    def hintButtonFunction(self,counter = 0):
        try:
            domainList = [str(i) for i in range(1, self.gameSize + 1)]
            row = int(random.choice(domainList))
            col = int(random.choice(domainList))
            if counter > self.gameSize:
                pass
            cellLineEdit = self.temporaryGameBoard.cellWidget(row-1, col-1).solutionLineEdit
            print("cell Text = ",cellLineEdit.text())
            if cellLineEdit.text() == " ":
                answer = self.solution[row-1][col-1]
                print("answer = ", answer)
                cellLineEdit.setText(str(answer))

            else:
                counter += 1
                self.hintButtonFunction(counter = counter)


        except Exception as e:
            print(e)

    def setGameFinalSolution(self,solution):
        self.solution = solution