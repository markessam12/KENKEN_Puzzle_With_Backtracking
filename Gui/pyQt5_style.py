from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import  *

class Label(QLabel):
    def __init__(self ,text ,fontSize = 18 ,setBold= False):
        super(Label, self).__init__()
        font = QFont("Arial" ,fontSize)
        font.setBold(setBold)
        self.setText(text)
        self.setFont(font)
        self.setAlignment(Qt.AlignCenter)

class GameBoardTable(QTableWidget):
    def __init__(self ,gameSize):
        super(GameBoardTable, self).__init__()
        # --- setting gameBoard size ---
        self.setRowCount(gameSize)
        self.setColumnCount(gameSize)

        # ---remove index of row &col ---
        self.verticalHeader().setVisible(False)
        self.horizontalHeader().setVisible(False)
        self.setFocusPolicy(Qt.NoFocus)
        self.setStyleSheet("QTableWidget::item{ selection-background-color: transparent;}")
        # dummyData is needed for setting background color for each cage
        for row in range(gameSize):
            for col in range(gameSize):
                # this empty string will be like zero in self.grid
                self.setItem(row,col,QTableWidgetItem(" "))

        # Make the table widget shrink to fit the table
        self.setSizeAdjustPolicy(self.AdjustToContents)
        self.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)

        # ---- squared cells ---
        self.horizontalHeader().setDefaultSectionSize(70)
        self.verticalHeader().setDefaultSectionSize(70)

        self.horizontalHeader().setDefaultAlignment(Qt.AlignHCenter)

class Layout(QVBoxLayout):
    def __init__(self):
        super(Layout, self).__init__()
        self.setSpacing(0)

class Widget(QWidget):
    def __init__(self):
        super(Widget, self).__init__()

class PushButton(QPushButton):
    def __init__(self ,buttonText ,picturePath =None):
        super(PushButton, self).__init__()
        textFont = QFont("Arial" ,18)
        textFont.setBold(True)

        if picturePath is not None:
            self.setIcon(QIcon(picturePath))
            self.setIconSize(QSize(25, 25))

        self.setText(buttonText)
        self.setFont(textFont)

class KenKenComboBox(QComboBox):
    def __init__(self ,placeHolder ,listToFill):
        super(KenKenComboBox, self).__init__()

        self.addItem(placeHolder)
        self.addItems(listToFill)
        self.setEditable(True)
        line_edit = self.lineEdit()
        # setting line edit alignment to the center
        line_edit.setAlignment(Qt.AlignCenter)

        # setting line edit to read only
        line_edit.setReadOnly(True)

        self.model().item(0).setEnabled(False)

class GameBoardLayout(QVBoxLayout):
    """This class takes game size ,cages dictionary and create the layout of the game with suitable Table as a gameBoard,
    it uses a function to color each cage with the color needed, each cell in the table is a comboBox it self include
    possible values can be used inside each cell of the table
    comboBoxes in table cells will be used later for playing not only solving kenken puzzle"""
    def __init__(self, gameSize, cagesDict):
        super(GameBoardLayout, self).__init__()
        # tableBoard is needed
        self.gameBoard = GameBoardTable(gameSize)

class StandardLineEdit(QLineEdit):
    def __init__(self,text = " ",ReadOnly = True, fontSize = None,borderColor = None):
        super().__init__()
        self.setText(text)
        self.setReadOnly(ReadOnly)
        self.adjustSize()
        self.setFixedHeight(53)
        if ReadOnly: # value + op
            self.setFixedHeight(17)

        self.setStyleSheet("{ border: none }")

        if fontSize is not None:
            font = Font(size= fontSize,setBold =False)
            self.setFont(font)
            self.setAlignment(Qt.AlignCenter)



class StandardComboBox (QComboBox):
    def __init__(self):
        super(StandardComboBox, self).__init__()

        font = Font()
        self.adjustSize()
        self.setFixedHeight(51.6)
        self.setStyleSheet("padding:0px" "QComboBox""{""border : 0.1px transparent""}")
        self.setStyleSheet("QComboBox::drop-down:button{border-radius:0px; background:transparent}")
        self.setEditable(True)
        lineEdit = self.lineEdit()

        # setting line edit alignment to the center
        lineEdit.setAlignment(Qt.AlignCenter)
        # setting line edit to read only
        lineEdit.setFont(font)
        lineEdit.setReadOnly(True)

class Font(QFont):
    def __init__(self,fontType = "Arial",size = 12, setBold = True):
        super(Font, self).__init__(fontType, size)
        self.setBold( setBold )

class BoardCellWidget(QWidget):
    def __init__(self, color = None,initialDomainSize = None,cageString = None):
        super(BoardCellWidget, self).__init__()
        layout = QFormLayout()

        # adjust spacings to your needs
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        # lineEdit Widget for writing cage operation and value
        font = Font(fontType = "Helvetica [Cronyx]",size = 13)

        self.lineEdit = StandardLineEdit()
        self.solutionLineEdit = StandardLineEdit(ReadOnly= False,fontSize= 16)
        self.solutionLineEdit.setValidator(QIntValidator(0,initialDomainSize))

        if color is not None:
            self.solutionLineEdit = StandardLineEdit(ReadOnly=False, fontSize=16,borderColor= color)
            self.lineEdit.setStyleSheet("QLineEdit" "{" "background : %s ;" "}"
                                        "QLineEdit""{""border : 0px %s;""}"%(color,color))
            self.solutionLineEdit.setStyleSheet("QLineEdit" "{" "background : %s ;" "}"
                                        "QLineEdit""{""border : 5px %s;""}"%(color,color))

        if cageString is not None:
            self.lineEdit.setFont(font)
            self.lineEdit.setText(cageString)

        layout.addRow(self.lineEdit)
        layout.addRow(self.solutionLineEdit)

        self.setLayout(layout)