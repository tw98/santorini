from turn import Turn
from memento import Caretaker
from players import PlayerFactory
from board import Board
import heuristics as h
from utils import UNDO, REDO, NEXT, reverse_direction

class GameEngine:
    def __init__(self, player1_type, player2_type, undo_redo, enable_score) -> None:
        self._turn = 1
        self._history = []
        player_factory = PlayerFactory()

        self._player_pieces = {
            'white': ['A', 'B'],
            'blue': ['Y', 'Z']
        }

        self._players = [
            player_factory.create_player(player1_type, self._player_pieces['white'], 'white'),
            player_factory.create_player(player2_type, self._player_pieces['blue'], 'blue')
        ]

        self.board = Board()

        self._current_player = None

        # game settings
        self._undo_redo = False
        if undo_redo == 'on':
            self._undo_redo = True

        self._enable_score = False
        if enable_score == 'on':
            self._enable_score = True

        self._caretaker = Caretaker(self.board)


    def _setup(self):
        '''
        Set starting positions of each player's pieces on the board
        '''
        player1_worker1 = self._players[0].workers[0]
        player1_worker2 = self._players[0].workers[1]
        player2_worker1 = self._players[1].workers[0]
        player2_worker2 = self._players[1].workers[1]
        self.board.setup(player1_worker1, player1_worker2, player2_worker1, player2_worker2)

    def _increment_turn(self):
        self._turn += 1

    def _decrement_turn(self):
        self._turn -= 1

    def _game_is_over(self):
        '''
        Check to see if the game is over according to game rules
        '''
        # game winning position
        winning_worker = self.board.check_game_winning_position()
        if winning_worker:
            for player in self._players:
                if winning_worker in player.workers:
                    print(f'{player.color} has won')
                    return True
            print('ERROR: should never get here')

        # check if current player doesn't have any actions to move
        if (self._current_player) and (not self._current_player.player_move_actions(self.board)):
            # if True, opponent player won the game
            print(f'{self._players[self._turn%2].color} has won')
            return True

        return False

    def _display_current_game_state(self):
        '''
        Display the current state of the board, turn number, and player turn
        '''
        self.board.display()
        color = self._current_player.color
        workers = ''.join(self._current_player.workers)

        output = f'Turn: {self._turn}, {color} ({workers})'

        if self._enable_score:
            height_score = h.height_score(self.board, self._current_player.workers)
            center_score = h.center_score(self.board, self._current_player.workers)
            dist_score = h.distance_score(self.board, self._current_player.workers)
            output += f', ({height_score}, {center_score}, {dist_score})'
        print(output)

    def _undo_turn(self):
        if self._caretaker.undo():
            self._decrement_turn()

    def _redo_turn(self):
        if self._caretaker.redo():
            self._increment_turn()

    def _next_turn(self):
        worker, move_dir, build_dir = self._current_player.make_move(self.board)
        self._caretaker.backup(worker, move_dir, build_dir)
        self._increment_turn()

    def _get_undo_redo_next(self):
        while True:
            choice = input("undo, redo, or next\n")
            if choice in [UNDO, REDO, NEXT]:
                return choice
            else:
                print("That is not a valid choice")

    def _flush_game_history(self):
        '''
        Delete any invalidated moves.
        '''
        if self._turn != len(self._history):
            self._history = self._history[:self._turn]

    def run(self):
        self._setup()

        while (True):
            self._current_player = self._players[(self._turn-1) % 2]

            self._display_current_game_state()

            if self._game_is_over():
                break

            if self._undo_redo:
                turn_type = self._get_undo_redo_next()
                if turn_type == NEXT:
                    self._flush_game_history()
                    self._next_turn()
                elif turn_type == UNDO:
                    self._undo_turn()
                elif turn_type == REDO:
                    self._redo_turn()
            else:
                self._next_turn()

            # self._increment_turn()
        
