import heuristics
import random

DIRECTIONS = ['n', 'ne', 'e', 'se', 's', 'sw', 'w', 'nw']


class MoveUtil:
    def __init__(self, worker, move_direction) -> None:
        self.worker = worker
        self.move_direction = move_direction
        # self.build_direction = build_direction

    def reverse_move(self):
        reverse_dir = {
            'n': 's', 'ne': 'sw', 'e': 'w', 'se': 'nw', 
            's': 'n', 'sw': 'ne', 'w': 'e', 'nw': 'se'
            }

        reverse_mov_d = reverse_dir[self.move_direction]
        # reverse_build_d = reverse_dir[self.build_direction]
        
        return reverse_mov_d #, reverse_build_d

class Move:
    def __init__(self, worker, move_direction, build_direction) -> None:
        self.worker = worker
        self.move_direction = move_direction
        self.build_direction = build_direction

    def reverse_move(self):
        reverse_dir = {
            'n': 's', 'ne': 'sw', 'e': 'w', 'se': 'nw', 
            's': 'n', 'sw': 'ne', 'w': 'e', 'nw': 'se'
            }

        reverse_mov_d = reverse_dir[self.move_direction]
        reverse_build_d = reverse_dir[self.build_direction]
        
        return reverse_mov_d, reverse_build_d

######### Player class & subclasses #########

class Player:
    '''
    DESIGN PATTERN: TEMPLATE
    '''

    def __init__(self, workers, color, report_move_summary=False) -> None:
        self.workers = workers
        self.color = color
        self.report_move_summary = report_move_summary

    def has_worker(self, worker):
        return worker in self.workers

    def player_move_actions(self, board):
        '''
        Gets a list of valid moves for each of the player's worker,
        according to the current board state
        '''
        moves_dict = {}
        for worker in self.workers:
            valid_moves = board.get_valid_moves(worker)
            if valid_moves:
                moves_dict[worker] = valid_moves
        return moves_dict

    def make_move(self, board):
        '''
        Sequence of actions:
        1. Get player's choice of what worker to move where
        2. Update the board with the valid choices
        3. Get player's choice of where to build
        4. Update the baord with the valid choice
        '''
        
        worker, mv_d = self._get_worker_move(board)
        board.move_worker(worker, mv_d)
        build_d = self._get_build_direction(board, worker)
        board.increment_building_height(worker, build_d)

        # print move summary if non-human player
        if self.report_move_summary:
            print(f'{worker},{mv_d},{build_d}')
        return Move(worker, mv_d, build_d)

    def _get_worker_move(self, board):
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

    # def is_valid_move_direction(self, d, board, worker):
    #     '''
    #     Check that the given direction is valid for the given worker to move
    #     Use case: Human
    #     '''
    #     if d in board.get_valid_moves(worker):
    #         return True
    #     return False

    def _is_valid_build_direction(self, d, board, worker):
        '''
        Check that the given direction is valid for the given worker to build
        Use case: Human
        '''
        if d in board.get_valid_builds(worker):
            return True
        return False

    def _get_worker_move(self, board):
        '''
        Pick a valid worker to move and a valid direction to move in.
        Repeats prompts until input is valid.
        '''
        valid_moves_dict = self.player_move_actions(board)
        
        # pick worker
        while True:
            choice_worker = input("Select a worker to move\n")

            player_has_worker = self.has_worker(choice_worker)
            if player_has_worker:
                if choice_worker in valid_moves_dict:
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
        '''
        Pick a valid direction to build in.
        Repeats prompts until input is valid.
        '''
        while True:
            choice = input("Select a direction to build (n, ne, e, se, s, sw, w, nw)\n")
            if choice not in DIRECTIONS:
                print("Not a valid direction")
            elif self._is_valid_build_direction(choice, board, worker):
                return choice
            else:
                print("Cannot build {0}".format(choice))
    

###
# GET STUCK IF PLAYER CHOOSES PLAYER WITHOUT VALID MOVES 
# WHILE OTHER PLAYER STILL HAS VALID MOVES
###
class RandomPlayer(Player):
    def __init__(self, workers, color) -> None:
        super(RandomPlayer, self).__init__(workers, color, report_move_summary=True)

    def _get_worker_move(self, board):
        '''
        Pick a valid worker to move and a valid direction to move in.
        Picks randomly among computed valid choices.
        '''
        moves_dict = self.player_move_actions(board)

        valid_workers = list(moves_dict.keys())
        worker = random.choice(valid_workers)

        return worker, random.choice(moves_dict[worker])

    def _get_build_direction(self, board, worker):
        '''
        Pick a valid direction to build in.
        Picks randomly among computed valid choices.
        '''
        valid_builds = board.get_valid_builds(worker)
        return random.choice(valid_builds)


class HeurisitcsPlayer(Player):
    def __init__(self, workers, color) -> None:
        super(HeurisitcsPlayer, self).__init__(workers, color, report_move_summary=True)

    def _get_worker_move(self, board):
        valid_moves_dict = self.player_move_actions(board)
        optimal_worker = None
        optimal_move_direction = None
        best_move_score = float('-inf')

        for worker in valid_moves_dict:
            for move in valid_moves_dict[worker]:
                # make the hypothetical move
                board.move_worker(worker, move)

                # check if move would end game
                if board.get_building_height_of_worker(worker) == 3:
                    reverse_move = MoveUtil(worker, move).reverse_move()
                    board.move_worker(worker, reverse_move)
                    return worker, move
                
                # calculate move score
                move_score = heuristics.move_score(board, self.workers)
                if move_score > best_move_score:
                    optimal_worker = worker
                    optimal_move_direction = move
                    best_move_score = move_score
                elif move_score == best_move_score:
                    optimal_worker, optimal_move_direction = random.choice([
                        (optimal_worker, optimal_move_direction),
                        (worker, move)
                    ])

                # reverse the hypothetical move
                reverse_move = MoveUtil(worker, move).reverse_move()
                board.move_worker(worker, reverse_move)

        return optimal_worker, optimal_move_direction
            
    def _get_build_direction(self, board, worker):
        # Same as RandomPlayer
        valid_builds = board.get_valid_builds(worker)
        return random.choice(valid_builds)

