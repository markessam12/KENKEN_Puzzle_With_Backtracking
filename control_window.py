from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QApplication
from Gui.main_window import MainWindow
from Gui.kenkenBoard_window import KenkenGameWindow
from kenken import Kenken
import time
import sys

class Controller:

    def __init__(self):

        self.toolName = "ASU Kenken Solver"
        self.toolIcon = 'Gui/Images/kenkenIcon.PNG'
        self.demonstrate = False
        self.demoButtonCounter = 0
        self.timeToSleep = 0.4

        self.main_window = MainWindow(self.toolName,self.toolIcon)



    def showMainWindow(self):

        self.main_window.show()
        self.main_window.startGameButton.clicked.connect(self.showKenkenGameWindow)


    def showKenkenGameWindow(self,):

        self.gameSize = self.main_window.getGameSize()
        self.gameAlgorithm = self.main_window.getGameAlgorithmType()

        self.kenkenSolver = Kenken(self.gameSize,self)
        cagesDict = self.kenkenSolver.getKenkenCagesDict()

        self.kenkenWindow = KenkenGameWindow(self.toolName, self.toolIcon)

        if self.main_window.error == False:
            self.main_window.hide()
            self.kenkenWindow.createKenkenGameLayout(gameSize= self.gameSize,cagesDict=cagesDict)
            self.kenkenWindow.show()

            # self.solveGameFunction()
            self.kenkenWindow.backButton.clicked.connect(self.backButtonFunction)
            self.kenkenWindow.solveButton.clicked.connect(self.printSolution)
            self.kenkenWindow.checkButton.clicked.connect(self.hintButtonFunction)
            self.kenkenWindow.ClearGame.triggered.connect(self.clearDemo)

    def backButtonFunction(self):
        self.kenkenWindow.hide()
        self.kenkenWindow.destroy()
        self.showMainWindow()

    # --- wrapper Functions to abstract FrontEnd from Backend ---
    def checkSolutionButtonFunction(self):
        pass

    def solveGameFunction(self):
        # --- different algorithms ---
        forwardChecking = False
        arcConsistency = False
        if self.gameAlgorithm == "ForwardChecking":
            forwardChecking = True
        elif self.gameAlgorithm == "ArcConsistency":
            arcConsistency = True
            forwardChecking = True

        self.kenkenSolver.solve(forward_check= forwardChecking, arc_consistency= arcConsistency)
        self.solvedGrid = self.kenkenSolver.getKenkenGrid()
        self.kenkenWindow.setGameFinalSolution(solution=self.solvedGrid)

    def printSolution(self):
        self.solveGameFunction()
        self.kenkenWindow.printFinalSolution(solution = self.solvedGrid)

    def setCell(self, row, col, value):
        self.kenkenWindow.setCellWindow(row, col, value)

        QApplication.processEvents()

        time.sleep(self.timeToSleep)

    def hintButtonFunction(self):
        self.demonstrate = True
        self.demoButtonCounter += 1
        if (self.demoButtonCounter > 3):
            # decrease speed time to its ititialized value again
            self.clearDemo()
        self.timeToSleep = self.timeToSleep / 2


        self.solveGameFunction()

    def clearDemo(self):
        # initialize time to solve to be as first time again
        self.timeToSleep = 0.4
        self.demoButtonCounter = 0
        self.demonstrate = False

def main():

    app = QApplication(sys.argv)
    flagX = 100


    while flagX == 100:

        controller = Controller()
        controller.showMainWindow()

        flagX = app.exec_()

    app.quit()
    sys.exit(flagX)



if __name__ == '__main__':
    main()