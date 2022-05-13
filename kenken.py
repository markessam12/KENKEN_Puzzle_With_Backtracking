import random

class Kenken:
    def __init__(self, n=3):
        """
        grid: 2d list of current existing numbers, zeros for empty cells
        cage: dictionary of dictionaries representing cages in the kenken puzzle. ex: {1:{value:5,op:'+',cells:[(0,0),(0,1),(1,0)]}}
        """
        #Zamala needs to type a hardcoded example here for trials
       cage = {
            1: {"value" :4, "op":'+',   "cells":[(0,0),(1,0)]},
            2: {"value" :5, "op":'+',   "cells":[(0,1),(1,1)]},
            3: {"value" :2, "op":'none',"cells":[(0,2)]}, #this sell has no operation
            4: {"value" :3, "op":'+',   "cells":[(2,0),(2,1)]},
            5: {"value" :4, "op":'+',   "cells":[(1,2),(2,2)]}
         }
          grid=[[1,3,2],[3,2,1],[2,1,3]]
        (self.grid, self.cage) = self.generate(self,random.randint(3, 9))
        self.n = len(self.grid)
        #3D list for the domain of available values for each cell (1d for each cell in the 2d grid)
        self.domains = [[[True for i in range(1, self.n+1)]]*self.n]*self.n
        """
        Example:
        [
        [[True, True, True], [True, True, True], [True, True, True]],
        [[True, True, True], [True, True, True], [True, True, True]],
        [[True, True, True], [True, True, True], [True, True, True]]
        ]
        """

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
        :return: True if col constraint is applied: No repeated values
        """
        # --- Default: Column constraint is applied ---
        isConstraintApplied = True
        # --- Iterate over each row ---
        for row in range(self.n):
            # --- check if there is a repeated value ---
            if self.grid[row][col] == value:
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
        if forward_check and not arc_consistency:
            self.backtracking_FC()
        elif forward_check and arc_consistency:
            pass
        elif not forward_check and not arc_consistency:
            self.backtracking()

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

    def backtracking_FC(self):
        row, col = self.find_empty()
        # Base case
        if row is None:
            return True

        # iterate over all possible values in the domain to test them
        for value in range(1, self.n+1):
            # check if the current value is in the domain of the cell
            if self.domains[row][col][value]:
                # check if the current value will obey all constrains
                if self.Bounding(row, col, value):
                    self.grid[row][col] = value
                    # forward checking the current value in all the neighbouring cells
                    self.forward_check(row, col, value, setting=False)
                    if self.backtracking():
                        return True
                    # return the removed value to the domains of the neighbouring cells
                    self.forward_check(row, col, value, setting=True)

        # backtrack the value
        self.grid[row][col] = 0
        return False

    def forward_check(self, row, col, value, setting=False):
        for i in range(1, self.n + 1):
            self.domains[i][col][value] = setting
            self.domains[row][i][value] = setting


    #Zamala
    def print(self):
        pass

    # Engy
    def find_empty(self):
        """
        :return: first empty position to use it next
        """
        # --- Loop over each cell position and check its value ---
        for row in range(self.n):
            for col in range(self.n):
                # --- if cellValue is "0" means empty cell ---
                cellValue = self.grid[row][col]
                # --- typeCasting "int()" to ensure that if condition is valid in case the self.grid 2-D list
                #     is initialized by "0" value as a string ---
                if int(cellValue) == 0:
                    # --- return first empty position to work on it next ---
                    return (row,col)
        return (None,None)
    #Engy
    def findListOfEmptyPositions(self):
        """
        This list return list of tuples containing all cells' positions has "0"(zero) value.
        Where "zero" in our kenkenSolver means undefined value or EMPTY CELL.
        :return: emptyPositionsList
        """
        emptyPositionsList = []
        # --- Loop over each cell position and check its value ---
        for row in range(self.n):
            for col in range(self.n):
                # --- if cellValue is "0" means empty cell ---
                cellValue = self.grid[row][col]
                # --- typeCasting "int()" to ensure that if condition is valid in case the self.grid 2-D list
                #     is initialized by "0" value as a string ---
                if int(cellValue) == 0:
                    # --- append empty position in emptyPositionsList ---
                    emptyPositionsList.append((row,col))

        return emptyPositionsList
