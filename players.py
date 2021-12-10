import heuristics
from board import Board

class Move:
    def __init__(self, worker, move_direction, build_direction, is_human=False) -> None:
        self.worker = worker
        self.move_direction = move_direction
        self.build_direction = build_direction
        self.human_move = is_human

DIRECTIONS = ['n', 'ne', 'e', 'se', 's', 'sw', 'w', 'nw']

class Player:
    def __init__(self, workers, color) -> None:
        self.workers = workers
        self.color = color

    def has_worker(self, worker):
        return worker in self.workers

    def make_move(self, board):
        worker = self._get_worker(board)
        mv_d = self._get_move_direction(board, worker)

        board.move_worker(worker, mv_d)
        board.display()
        build_d = self._get_build_direction(board, worker)

        board.increment_building_height(worker, build_d)
        return Move(worker, mv_d, build_d)

    def _get_worker(self, board):
        raise NotImplementedError
    
    def _get_move_direction(self,board):
        raise NotImplementedError

    def _get_build_direction(self, board):
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

    def _get_worker(self, board):
        while True:
            choice = input("Select a worker to move\n")

            player_has_worker = self.has_worker(choice)
            if player_has_worker:
                return choice
            else:
                if choice in board.get_all_workers_in_game():
                    print("That is not your worker")
                else:
                    print("Not a valid worker")
    
    def _get_move_direction(self, board, worker):
        while True:
            choice = input("Select a direction to move (n, ne, e, se, s, sw, w, nw)\n")
            if choice not in DIRECTIONS:
                print("Not a valid direction")
            elif board.is_valid_move_direction(choice, worker):
                return choice
            else:
                print("Cannot move {0}".format(choice))

    def _get_build_direction(self, board, worker):
        while True:
            choice = input("Select a direction to build (n, ne, e, se, s, sw, w, nw)\n")
            if choice not in DIRECTIONS:
                print("Not a valid direction")
            elif board.is_valid_build_direction(choice, worker):
                return choice
            else:
                print("Cannot build {0}".format(choice))
    

class RandomPlayer(Player):
    def __init__(self, workers, color) -> None:
        super(RandomPlayer, self).__init__(workers, color)

    def _get_worker(self, board):
        pass

    def _get_move_direction(self, board):
        pass

    def _get_build_direction(self, board):
        pass

class HeurisitcsPlayer(Player):
    def __init__(self, workers, color) -> None:
        super(HeurisitcsPlayer, self).__init__(workers, color)

    def _get_worker(self, board):
        pass

    def _get_move_direction(self, board):
        pass

    def _get_build_direction(self, board):
        pass

