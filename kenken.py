import random

class Kenken:
    def __init__(self):
        """
        grid: 2d list of current existing numbers, zeros for empty cells
        cage: dictionary of dictionaries representing cages in the kenken puzzle. ex: {1:{value:5,op:'+',cells:[(0,0),(0,1),(1,0)]}}
        """
        #Zamala needs to type a hardcoded example here for trials
        (self.grid, self.cage) = self.generate(self,random.randint(3, 9))

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
        responsible for Column checking, Row checking, and Grid checking
        :return: returns true if the current chosen numbers satisfy the game rules and false otherwise
        """
        pass

    #Engy
    def check_row(self, row, value):
        pass

    #Engy
    def check_column(self, col, value):
        pass

    #Eman
    def check_cage(self, raw, col, value):
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
    def backtracking(self, forward_check, arc_consistency):
        pass

    #Zamala
    def print(self):
        pass

    #Engy
    def find_empty(self):
        pass