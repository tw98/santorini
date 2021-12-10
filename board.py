import numpy as np

class Board:
    def __init__(self):
        self.__board = np.zeros((5,5))

    def display(self):
        separator = '+--+--+--+--+--+'
        for row in self.__board:
            for elt in row: 
                print('|')
                print(elt.ljust(2))
            print('|')
        print(separator)

    def is_valid_move_direction(self, d):
        return True

    def is_valid_build_direction(self, d):
        return True