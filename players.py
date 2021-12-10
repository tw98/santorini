import heuristics
from board import Board, Move

DIRECTIONS = ['n', 'ne', 'e', 'se', 's', 'sw', 'w', 'nw']

class Player:
    def __init__(self, workers, color) -> None:
        self.workers = workers
        self.color = color

    def has_worker(self, worker):
        return worker in self.workers

    def get_move(self, board):
        raise NotImplementedError

    def _get_worker(self):
        raise NotImplementedError
    
    def _get_move_direction(self):
        raise NotImplementedError

    def _get_build_direction(self):
        raise NotImplementedError


class PlayerFactory():
    def __init__(self) -> None:
        return

    def create_player(self, type, workers, color):
        if type == 'human':
            return HumanPlayer(workers, color)
        elif type == 'random':
            return RandomPlayer(workers, color)
        elif type == 'heuristic':
            return HeurisitcsPlayer(workers, color)
        else:
            print('Invalid type')
            exit(1)

class HumanPlayer(Player):
    def __init__(self, workers, color) -> None:
        super(HumanPlayer, self).__init__(workers, color)

    def get_move(self, board, game_workers):
        worker = self._get_worker_input(game_workers)
        move_direction = self._get_move_direction(board)
        build_direction = self._get_build_direction(board)
        return Move(worker, move_direction, build_direction)

    def _get_worker_input(self, game_workers):
        while True:
            choice = input("Select a worker to move\n")

            player_has_worker = self.has_worker(choice)
            if player_has_worker:
                return choice
            else:
                if choice in game_workers:
                    print("That is not your worker")
                else:
                    print("Not a valid worker")
    
    def _get_move_direction(self, board):
        while True:
            choice = input("Select a direction to move (n, ne, e, se, s, sw, w, nw)\n")
            if choice not in DIRECTIONS:
                print("Not a valid direction")
            elif board.is_valid_move_direction(choice):
                return choice
            else:
                print("Cannot move {0}".format(choice))

    def _get_build_direction(self, board):
        while True:
            choice = input("Select a direction to build (n, ne, e, se, s, sw, w, nw)\n")
            if choice not in DIRECTIONS:
                print("Not a valid direction")
            elif board.is_valid_build_direction(choice):
                return choice
            else:
                print("Cannot build {0}".format(choice))
    

class RandomPlayer(Player):
    def __init__(self, workers, color) -> None:
        super(RandomPlayer, self).__init__(workers, color)

class HeurisitcsPlayer(Player):
    def __init__(self, workers, color) -> None:
        super(HeurisitcsPlayer, self).__init__(workers, color)


