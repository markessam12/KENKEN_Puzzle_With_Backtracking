import random
from functools import reduce
from random import seed, random, shuffle, randint, choice
from collections import deque


class Kenken:
    def __init__(self, n=3, controller=None):
        """
        grid: 2d list of current existing numbers, zeros for empty cells
        cage: dictionary of dictionaries representing cages in the kenken puzzle. ex: {1:{value:5,op:'+',cells:[(0,0),(0,1),(1,0)]}}
        """
        self.grid = [[0 for i in range(n)] for j in range(n)]

        self.cages, self.ans = self.generate(n)
        self.n = n
        self.controller = controller
        # --- 2D array, each cell position has cage number as its value ---
        self.cellToCageMap = self.mapCellsToCages()
        

        #3D list for the domain of available values for each cell (1d for each cell in the 2d grid)
        self.domains = [[[True for i in range(n)] for j in range(n)] for k in range(n)]
        """
        Example:
        [
        [[True, True, True], [True, True, True], [True, True, True]],
        [[True, True, True], [True, True, True], [True, True, True]],
        [[True, True, True], [True, True, True], [True, True, True]]
        ]
        """

        self.queues = deque()

    def operation(self, operator):
        """
        A utility function used in order to determine the operation corresponding
        to the operator that is given in string format
        """
        if operator == '+':
            return lambda a, b: a + b
        elif operator == '-':
            return lambda a, b: a - b
        elif operator == '*':
            return lambda a, b: a * b
        elif operator == '/':
            return lambda a, b: a / b
        else:
            return None

    def adjacent(self, xy1, xy2):
        """
        Checks wheither two positions represented in 2D coordinates are adjacent
        """
        x1, y1 = xy1
        x2, y2 = xy2

        dx, dy = x1 - x2, y1 - y2

        return (dx == 0 and abs(dy) == 1) or (dy == 0 and abs(dx) == 1)

    def generate(self, size):
        """
        Generate a random kenken puzzle of the given size
          * Initially create a latin square of size 'size' and elements the values [1...size]
          * Shuffle the board by rows and columns in order to get a somewhat random
            board that still satisfies the different row-col constraint of kenken
          * Initialize the 'uncaged' set with all cell coordinates
          * Proceed in creating cliques:
            * Randomly choose a clique size in the range [1..4]
            * Set the first cell in the 'uncaged' set in row major order as
              the root cell of the clique and remove it from the 'uncaged' set
            * Randomly visit at most 'clique-size' 'uncaged' adjacent cells
              in random directions while adding them to the current clique
              and removing them from the 'uncaged' cells
            * The size of the resulting clique is:
              * == 1:
                there is no operation to be performed and the target of the clique
                is equal to the only element of the clique
              * == 2:
                * if the two elements of the clique can be divided without a remainder
                  then the operation is set to division and the target is the quotient
                * otherwise, the operation is set to subtraction and the target is the
                  difference of the elements
              * >  2:
               randomly choose an operation between addition and multiplication.
                The target of the operation is the result of applying the decided
                operation on all the elements of the clique
            * Continue until the 'uncaged' set is empty i.e. there is no cell belonging
              to no clique
        """

        board = [[((i + j) % size) + 1 for i in range(size)] for j in range(size)]

        for _ in range(size):
            shuffle(board)

        for c1 in range(size):
            for c2 in range(size):
                if random() > 0.5:
                    for r in range(size):
                        board[r][c1], board[r][c2] = board[r][c2], board[r][c1]

        board = {(j + 1, i + 1): board[i][j] for i in range(size) for j in range(size)}

        uncaged = sorted(board.keys(), key=lambda var: var[1])

        cliques = []
        while uncaged:

            cliques.append([])

            csize = randint(1, 4)

            cell = uncaged[0]

            uncaged.remove(cell)

            cliques[-1].append(cell)

            for _ in range(csize - 1):

                adjs = [other for other in uncaged if self.adjacent(cell, other)]

                cell = choice(adjs) if adjs else None

                if not cell:
                    break

                uncaged.remove(cell)

                cliques[-1].append(cell)

            csize = len(cliques[-1])
            if csize == 1:
                cell = cliques[-1][0]
                cliques[-1] = ((cell, ), '.', board[cell])
                continue
            elif csize == 2:
                fst, snd = cliques[-1][0], cliques[-1][1]
                if board[fst] / board[snd] > 0 and not board[fst] % board[snd]:
                    operator = "/" # choice("+-*/")
                else:
                    operator = "-" # choice("+-*")
            else:
                operator = choice("+*")

            target = reduce(self.operation(operator), [board[cell] for cell in cliques[-1]])

            cliques[-1] = (tuple(cliques[-1]), operator, int(target))

        full_dect = {}
        inside_dect = {}
        inside_dect["value"] = 0
        inside_dect["op"] = 0
        inside_dect["cells"] = []
        iterator = 1
        for i in range(0,len(cliques)):
            if cliques[i][2] <  0:
                inside_dect["value"] = abs(cliques[i][2])
            else:
                inside_dect["value"] =  cliques[i][2]

            if(cliques[i][1] == '.'):
                inside_dect["op"] = "none"
            else:
                inside_dect["op"] = cliques[i][1]

            temp_list = []
            for j in cliques[i][0]:
                y = list(j)
                y[0] = y[0]-1
                y[1] = y[1]-1
                x = tuple(y)
                temp_list.append(x)

            inside_dect["cells"] = temp_list
            full_dect[iterator]=inside_dect.copy()
            iterator= iterator+1

        return full_dect, board

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

    def check_cage(self, row, col, value):

        """This function takes parameters specifies cell position and the value inside this cell,
        check the cage of this cell by searching in cellToCageMap 2D array , then access this cage to
        ensure that this value relative to all other cells in the same cage satisfy cage operation
        and constraint or not. if satisfied it return "True", else it return "False"
        """
        isConstraintApplied =False
        # search with the row and col (cell position in cellToCageMap 2D array to get cage number
        cageNumber = self.cellToCageMap[row][col]
        cageNeededToBeChecked = self.cages.get(cageNumber)
        # get cellsList of the cage
        cellsList = cageNeededToBeChecked['cells']
        # get cage operation
        cageOperation = cageNeededToBeChecked['op']

        # FreeBie
        if cageOperation == "none": # freeBie
            # index of [0] is used because cellsList of this cage contains only ONE cell(freeBie)
            if int(value) == int(cageNeededToBeChecked['value']):
                isConstraintApplied = True

        # ADDITION
        elif cageOperation == "+" : # cellsList > = 2
            summationResult = 0
            zerosCount = 0
            for cell in cellsList: # cell is tuple (1,2)
                if (row,col) != cell: # sum all cells except the one Iam checking
                    zerosCount += (self.grid[cell[0]][cell[1]] == 0)
                    summationResult += int(self.grid[cell[0]][cell[1]])
            if zerosCount and summationResult + int(value) < int(cageNeededToBeChecked['value']):
                isConstraintApplied = True
            elif not zerosCount and summationResult + int(value) == int(cageNeededToBeChecked['value']):
                isConstraintApplied = True

        # SUBTRACTION
        elif cageOperation == "-": # cellsList has only 2 cells according to game Rules
            subtractionResult = 0
            for cell in cellsList:
                if (row,col) != cell : # I have this cell value passed to my function
                    if self.grid[cell[0]][cell[1]] == 0:
                        isConstraintApplied = True
                        break
                    subtractionResult = int(value) - int(self.grid[cell[0]][cell[1]])
            # check if constraint is applied
            if abs(subtractionResult) == cageNeededToBeChecked['value']:
                isConstraintApplied = True

        # MULTIPLICATION
        elif cageOperation == "*": # cellsList > = 2
            multiplicationResult = 1
            zerosCount = 0
            for cell in cellsList:
                if (row,col) != cell:
                    if self.grid[cell[0]][cell[1]] == 0:
                        zerosCount += 1
                    else:
                        multiplicationResult *= self.grid[cell[0]][cell[1]]

            if zerosCount and multiplicationResult * value <= cageNeededToBeChecked['value']:
                isConstraintApplied = True
            elif not zerosCount and multiplicationResult * value == cageNeededToBeChecked['value']:
                isConstraintApplied = True

        # DIVISION
        elif cageOperation == "/": # cellsList = 2
            divisionResult = 1
            for cell in cellsList:
                if (row,col) != cell : # I have this cell value passed to my function
                    if self.grid[cell[0]][cell[1]] == 0:
                        isConstraintApplied = True
                        break
                    elif value > self.grid[cell[0]][cell[1]]:
                        # divide greater/smaller
                        divisionResult = value / self.grid[cell[0]][cell[1]]
                    else:
                        # divide greater/smaller
                        divisionResult = self.grid[cell[0]][cell[1]] / value
            # check if constraint is applied
            if divisionResult == cageNeededToBeChecked['value']:
                isConstraintApplied = True

        return isConstraintApplied

    def mapCellsToCages(self):
        """
        :return: A function return a 2d list with the cage number at each cell position
        """
        gameSize = len(self.grid)
        cellToCageMap = [ [0]*gameSize for i in range(gameSize)] # --- number of all cells in the game ---
        for cage in self.cages:
            cellsOfCageTupleList = self.cages[cage]['cells']  # --- cellsOfCage is list of tuples ---
            for cellTuple in cellsOfCageTupleList:
                row = cellTuple[0]
                col = cellTuple[1]
                cellToCageMap[row][col] = cage

        return cellToCageMap

    def solve(self, forward_check = False, arc_consistency=False):
        """
        a wrapper function that calls the recursive backtracking function
        :param forward_check: enable forward checking mode
        :param arc_consistency: enable arc consistency mode
        :return:
        """
        self.grid = [[0 for i in range(self.n)] for j in range(self.n)]
        self.domains = [[[True for i in range(self.n)] for j in range(self.n)] for k in range(self.n)]
        if forward_check and not arc_consistency:
            self.backtracking_FC()
        elif forward_check and arc_consistency:
            self.backtracking_AC_FC()
        elif not forward_check and not arc_consistency:
            self.backtracking()

    def backtracking(self):
        """
        :return: a recursive function that return True when a solution is found
        """
        row, col = self.find_empty()
        # Base case
        if row is None:
            return True

        # iterate over all possible values to test them
        for i in range(1, self.n + 1):
            # check if the current value will obey all constrains
            if self.controller.demonstrate:
                self.controller.setCell(row, col, i)
            if self.Bounding(row, col, i):
                self.grid[row][col] = i
                if self.backtracking():
                    return True

        # backtrack the value
        self.grid[row][col] = 0
        if self.controller.demonstrate:
            self.controller.setCell(row, col, ' ')
        return False

    def backtracking_FC(self):
        """
        :return: a recursive function that return True when a solution is found that supports forward checking
        """
        row, col = self.find_empty()
        # Base case
        if row is None:
            return True

        # iterate over all possible values in the domain to test them
        for value in range(self.n):
            # check if the current value is in the domain of the cell
            if self.domains[row][col][value]:
                if self.controller.demonstrate:
                    self.controller.setCell(row, col, value + 1)
                # check if the current value will obey all constrains
                if self.Bounding(row, col, value + 1):
                    self.grid[row][col] = value + 1
                    # forward checking the current value in all the neighbouring cells
                    self.forward_check(row, col, value, setting=False)
                    if self.backtracking_FC():
                        return True
                    # return the removed value to the domains of the neighbouring cells
                    self.forward_check(row, col, value, setting=True)

        # backtrack the value
        self.grid[row][col] = 0
        if self.controller.demonstrate:
            self.controller.setCell(row, col, ' ')
        return False

    def backtracking_AC_FC(self):
        """
        :return: A function that reduces the domains of variables using arc consistency and find the unique solution using backtracking and forward checking
        """
        # solve uniray constraints first:
        for cage in self.cages:
            if self.cages[cage]["op"] == 'none':
                row, col = self.cages[cage]["cells"][0]
                value = self.cages[cage]["value"]
                for i in range(self.n):
                    self.domains[row][col][i] = False
                self.forward_check(row, col, value - 1, setting=False)
                self.domains[row][col][value - 1] = True
        # Fill queue with all the releationships
        self.fill_queue()
        # Solve using AC3
        self.AC3()
        # Find final unique solution using backtracking and forward checking
        self.backtracking_FC()

    def constrain_check(self,ix,iy,jx,jy,a,b,constrain_type):
        """
        :param ix: row of variable Xi
        :param iy: col of variable Xi
        :param jx: row of variable Xj
        :param jy: col of variable Xj
        :param a: value of Xi in it's current domain
        :param b: value of Xj in it's current domain
        :param constrain_type: The type of the constraints between the two variables
        :return: boolean value that is True when a and b satisfy the constrain between Xi and Xj
        """
        result = True
        if constrain_type == '=':
            if (ix == jx or iy == jy) and a == b:
                result = False
        else:
            cage_number = self.cellToCageMap[ix][iy]
            if constrain_type == '+':
                result = (a + b) <= self.cages[cage_number]["value"]
            elif constrain_type == '-':
                result = abs(a - b) == self.cages[cage_number]["value"]
            elif constrain_type == '*':
                result = (a * b) <= self.cages[cage_number]["value"]
            elif constrain_type == '/':
                result = (max(a,b)/min(a,b)) == self.cages[cage_number]["value"]

        return result

    def revise(self, Xi,Xj,constrain_type):
        """
        :param Xi: First variable of the relation
        :param Xj: Second variable of the relation
        :param constrain_type: type of the relation
        :return:boolean that is true if the domain of Xi changed
        """
        changed = False
        for a in range(self.n):
            found = False
            if self.domains[Xi[0]][Xi[1]][a]:
                for b in range(self.n):
                    if self.domains[Xj[0]][Xj[1]][b]:
                        if self.constrain_check(Xi[0],Xi[1],Xj[0],Xj[1],a+1,b+1,constrain_type):
                            found = True
                            break
                if not found:
                    self.domains[Xi[0]][Xi[1]][a] = False
                    changed = True
        return changed
   
    def fill_queue(self):
        """
        :return: function that fills self.queues with the arcs between all the variables
        """
        for x in range(self.n):
            for y in range(self.n):
                for i in range(self.n):
                    # arcs of Xi with other variables in it's col
                    if y != i :
                        self.queues.append(([x, y], [x,i], '='))
                    # arcs of Xi with other variables in it's row
                    if x != i:
                        self.queues.append(([x, y], [i, y], '='))
                cage_number = self.cellToCageMap[x][y]
                # arcs of Xi with other variables in it's cage
                for cell in self.cages[cage_number]["cells"]:
                    if self.cages[cage_number]['op'] != 'none':
                        if not (cell[0] == x and cell[1] == y):
                            self.queues.append(([x, y], [cell[0], cell[1]], self.cages[cage_number]['op']))

    def AC3(self):
        """
        :return: A function that changes the self.domains (implementation of arc consistency algorithm)
        """
        # continue while Queue is not empty
        while len(self.queues):
            # select and delete an arc (Xi, Xj) from the queue
            arc = self.queues.popleft()
            # if Revise caused any changes to the domains then add all arcs that touch Xi to the queue
            if self.revise(arc[0], arc[1], arc[2]):
                x,y = arc[0]
                for i in range(self.n):
                    # arcs of Xi with other variables in it's col
                    if y != i :
                        if not ([x, y], [x,i], '=') in self.queues:
                            self.queues.append(([x, y], [x,i], '='))
                        if not ([x, i], [x, y], '=') in self.queues:
                            self.queues.append(([x, i], [x, y], '='))
                    # arcs of Xi with other variables in it's row
                    if x != i:
                        if not ([x, y], [i, y], '=') in self.queues:
                            self.queues.append(([x, y], [i, y], '='))
                        if not ([i, y], [x, y], '=') in self.queues:
                            self.queues.append(([i, y], [x, y], '='))
                cage_number = self.cellToCageMap[x][y]
                # arcs of Xi with other variables in it's cage
                for cell in self.cages[cage_number]["cells"]:
                    if self.cages[cage_number]['op'] != 'none':
                        if not (cell[0] == x and cell[1] == y):
                            if not ([x, y], [cell[0], cell[1]], self.cages[cage_number]['op']) in self.queues:
                                self.queues.append(([x, y], [cell[0], cell[1]], self.cages[cage_number]['op']))
                            if not ([cell[0], cell[1]],[x, y], self.cages[cage_number]['op']) in self.queues:
                                self.queues.append(([cell[0], cell[1]],[x, y], self.cages[cage_number]['op']))

    def forward_check(self, row, col, value, setting=False):
        """
        :param row: row of the current variable
        :param col: col of the current variable
        :param value: value of the current variable
        :param setting: boolean variable that set the function to enable or disable the domains
        :return:
        """
        for i in range(self.n):
            self.domains[i][col][value] = setting
            self.domains[row][i][value] = setting
        cage = self.cellToCageMap[row][col]
        # for r, c in self.cages[cage]['cells']:
        #     if (r != row) and (c != col):
        #         for v in range(self.n):
        #             # check if the current value is in the domain of the cell
        #             if self.domains[r][c][v] ^ setting:
        #                 if self.Bounding(r, c, v+1) == setting:
        #                     self.domains[r][c][v] = setting

    def print(self):
        """
        :return: printing funtion for debugging
        """
        print("self.grid =" ,self.grid)
        print("self.ans = ",self.ans)
        print("self.cages = ", self.cages)
    def getKenkenGrid(self):
        return self.grid

    def getKenkenCagesDict(self):
        return self.cages


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
