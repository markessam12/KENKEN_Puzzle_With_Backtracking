import random

class Kenken:
    def __init__(self):
        """
        grid: 2d list of current existing numbers
        cage: dictionary of dictionaries representing cages in the kenken puzzle. ex: {1:{value:5,op:'+',cells:[(0,0),(0,1),(1,0)]}}
        """
        (self.grid, self.cage) = self.generate(self,random.randint(3, 9))

    def generate(self, size):
        """
        :param size: the size of the generated grid
        :return: it creates and returns a random game (the data structure of the game is not decided yet)
        """
        pass

    def bounding(self):
        """
        responsible for Column checking, Row checking, and cage checking
        :return: returns true if the current chosen numbers satisfy the game rules and false otherwise
        """
        pass

    def check_row(self, row, value):
        pass

    def check_column(self, col, value):
        pass

    def check_cage(self, raw, col, value):
        pass


    def solve(self, forward_check=True, arc_consistency=True):
        """
        a wrapper function that calls the recursive backtracking function
        :param forward_check: enable forward checking mode
        :param arc_consistency: enable arc consistency mode
        :return:
        """
        pass

    def backtracking(self, forward_check, arc_consistency):
        pass

    def print(self):
        pass

    def find_empty(self):
        pass