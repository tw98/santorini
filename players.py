import heuristics
from board import Board
import random

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

    def player_move_actions(self, board):
        moves_dict = {}
        for worker in self.workers:
            valid_moves = board.get_valid_moves(worker)
            if valid_moves:
                moves_dict[worker] = valid_moves
        return moves_dict

    def make_move(self, board):
        worker, mv_d = self._get_worker_move(board)

        board.move_worker(worker, mv_d)
       
        build_d = self._get_build_direction(board, worker)

        board.increment_building_height(worker, build_d)
        return Move(worker, mv_d, build_d)

    def _get_worker(self, board):
        raise NotImplementedError
    
    def _get_move_direction(self,board, worker):
        raise NotImplementedError

    def _get_build_direction(self, board, worker):
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

    def _get_worker_move(self, board):
        valid_moves_dict = self.player_move_actions(board)
        
        # pick worker
        while True:
            choice_worker = input("Select a worker to move\n")

            player_has_worker = self.has_worker(choice_worker)
            if player_has_worker:
                if choice_worker in valid_moves_dict[choice_worker]:
                    # valid worker
                    break
                else:
                    print("Worker has no valid moves")
            else:
                if choice_worker in board.get_all_workers_in_game():
                    print("That is not your worker")
                else:
                    print("Not a valid worker")

        # pick direction
        while True:
            choice_direction = input("Select a direction to move (n, ne, e, se, s, sw, w, nw)\n")
            if choice_direction not in DIRECTIONS:
                print("Not a valid direction")

            elif choice_direction in valid_moves_dict[choice_worker]:
                # board.is_valid_move_direction(choice_direction, choice_worker):
                break
            else:
                print("Cannot move {0}".format(choice_direction))
        
        return choice_worker, choice_direction

    def _get_build_direction(self, board, worker):
        while True:
            choice = input("Select a direction to build (n, ne, e, se, s, sw, w, nw)\n")
            if choice not in DIRECTIONS:
                print("Not a valid direction")
            elif board.is_valid_build_direction(choice, worker):
                return choice
            else:
                print("Cannot build {0}".format(choice))
    
###
# GET STUCK IF PLAYER CHOOSES PLAYER WITHOUT VALID MOVES 
# WHILE OTHER PLAYER STILL HAS VALID MOVES
###
class RandomPlayer(Player):
    def __init__(self, workers, color) -> None:
        super(RandomPlayer, self).__init__(workers, color)

    def _get_worker_move(self, board):
        moves_dict = self.player_move_actions(board)

        valid_workers = list(moves_dict.keys())
        worker = random.choice(valid_workers)

        return worker, random.choice(moves_dict[worker])

    def _get_build_direction(self, board, worker):
        valid_builds = board.get_valid_builds(worker)
        return random.choice(valid_builds)

class HeurisitcsPlayer(Player):
    def __init__(self, workers, color) -> None:
        super(HeurisitcsPlayer, self).__init__(workers, color)

    def _get_worker_move(self, board):
        pass

    def _get_build_direction(self, board, worker):
        pass

