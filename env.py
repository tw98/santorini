from players import PlayerFactory
from board import Board

class GameEngine:

    DIRECTIONS = ['n', 'ne', 'e', 'se', 's', 'sw', 'w', 'nw']

    def __init__(self) -> None:
        self.__turn = 0
        self.__board = Board()
        self.__history = {}
        self.player1 = PlayerFactory(...)
        # player2
        self.__players = []
        self.__current_player = None

        player_factory = PlayerFactory()
        pass

    def __get_move_direction(self):
        while True:
            choice = input("Select a direction to move (n, ne, e, se, s, sw, w, nw)\n")
            if choice not in self.DIRECTIONS:
                print("Not a valid direction")
            elif self.__board.is_valid_move_direction(choice):
                return choice
            else:
                print("Cannot move {0}".format(choice))

    def __get_build_direction(self):
        while True:
            choice = input("Select a direction to build (n, ne, e, se, s, sw, w, nw)\n")
            if choice not in self.DIRECTIONS:
                print("Not a valid direction")
            elif self.__board.is_valid_build_direction(choice):
                return choice
            else:
                print("Cannot build {0}".format(choice))

    def increment_turn(self):
        self.__turn += 1

    def __game_is_over(self):
        return False

    def run():
        while (not self.__game_is_over()):
            self.__get_worker_input()
            self.__get_move_direction()
            self.__get_build_direction()
            self.__board.display()
        

if __name__ == "__main__":
    env = GameEngine()
    env.run()