import random

class Kenken:
    def __init__(self):
        """
        grid: 2d list of current existing numbers, zeros for empty cells
        cage: dictionary of dictionaries representing cages in the kenken puzzle. ex: {1:{value:5,op:'+',cells:[(0,0),(0,1),(1,0)]}}
        """
        #Zamala needs to type a hardcoded example here for trials
        (self.grid, self.cage) = self.generate(self,random.randint(3, 9))
        self.n = len(self.grid)

    #Tarek and Zamala
    def generate(self, size):
        """
        :param size: the size of the generated grid
        :return: it creates and returns a random game (the data structure of the game is not decided yet)
        """
        pass

    #Engy and Eman, Engy will start on the gui after her work on the constrain checking functions
    def Bounding(self, row, col, value):
        """
        Responsible for Column checking, Row checking, and Grid checking
        This function checks if all ken-ken puzzle constraints (rules) are applied or not.

        :param row: cell row position
        :param col: cell column position
        :param value: cell value
        :return: returns True if the current chosen numbers satisfy the game rules and false otherwise
        """

        isAllConstraintsApplied = False
        conditionsList = [self.check_row(row= row, value= value), # --- check row constraint ---
                          self.check_column(col= col, value= value), # --- check column constraint ---
                          self.check_cage(row= row, col= col, value= value)] # --- check cage operation constraint ---
        if all(conditionsList):
            isAllConstraintsApplied = True

        return isAllConstraintsApplied

    #Engy
    def check_row(self, row, value):
        """
        This function returns true iff row has no cell containing value same as the given value,
        and return false otherwise.
        NOTE: this function should be called before assigning a value in a cell by the solver
        :param row: row number
        :param value: value to check if present in the given row
        :return: True if row constraint is applied: No repeated values
        """
        # --- Default: Row constraint is applied ---
        isConstraintApplied = True
        # --- self.grid[row] is a 1-D list ---
        for columnItem in self.grid[row]:
            # --- check if there is a repeated value ---
            if columnItem == value:
                isConstraintApplied = False

        return isConstraintApplied


    #Engy
    def check_column(self, col, value):
        """
               This function returns true iff col has no cell containing value same as the given value,
               and return false otherwise.
               NOTE: this function should be called before assigning a value in a cell by the solver
               :param col: col number
               :param value: value to check if present in the given row
               :return: True if row constraint is applied: No repeated values
               """
        # --- Default: Column constraint is applied ---
        isConstraintApplied = True
        # --- self.grid[col] is a 1-D list ---
        for columnItem in self.grid[col]:
            # --- check if there is a repeated value ---
            if columnItem == value:
                isConstraintApplied = False

        return isConstraintApplied

    #Eman
    def check_cage(self, row, col, value):
        pass

    #Mark and Mark
    def solve(self, forward_check=True, arc_consistency=True):
        """
        a wrapper function that calls the recursive backtracking function
        :param forward_check: enable forward checking mode
        :param arc_consistency: enable arc consistency mode
        :return:
        """
        pass

    #Mark and Mark
    def backtracking(self):
        row, col = self.find_empty()
        # Base case
        if row is None:
            return True

        # iterate over all possible values to test them
        for i in range(1, self.n + 1):
            # check if the current value will obey all constrains
            if self.Bounding(row, col, i):
                self.grid[row][col] = i
                if self.backtracking():
                    return True

        # backtrack the value
        self.grid[row][col] = 0
        return False

    #Zamala
    def print(self):
        pass

    # Engy
    def find_empty(self):
        """
        :return: first empty position to use it next
        """
        boardSize = len(self.grid)
        # --- Loop over each cell position and check its value ---
        for row in range(boardSize):
            for col in range(boardSize):
                # --- if cellValue is "0" means empty cell ---
                cellValue = self.grid[row][col]
                # --- typeCasting "int()" to ensure that if condition is valid in case the self.grid 2-D list
                #     is initialized by "0" value as a string ---
                if int(cellValue) == 0:
                    # --- return first empty position to work on it next ---
                    return (row,col)
    #Engy
    def findListOfEmptyPositions(self):
        """
        This list return list of tuples containing all cells' positions has "0"(zero) value.
        Where "zero" in our kenkenSolver means undefined value or EMPTY CELL.
        :return: emptyPositionsList
        """
        emptyPositionsList = []
        # --- boardSize is needed to be dynamic depending on the random value that the user choose ---
        boardSize = len(self.grid)
        # --- Loop over each cell position and check its value ---
        for row in range(boardSize):
            for col in range(boardSize):
                # --- if cellValue is "0" means empty cell ---
                cellValue = self.grid[row][col]
                # --- typeCasting "int()" to ensure that if condition is valid in case the self.grid 2-D list
                #     is initialized by "0" value as a string ---
                if int(cellValue) == 0:
                    # --- append empty position in emptyPositionsList ---
                    emptyPositionsList.append((row,col))

        return emptyPositionsList