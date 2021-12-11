from players import PlayerFactory
from board import Board

class GameEngine:
    def __init__(self, player1_type, player2_type, undo_redo, enable_score) -> None:
        self._turn = 1
        self._history = {}
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
        self._undo_redo = undo_redo
        self._enable_score = enable_score

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
        print(f'Turn: {self._turn}, {color} ({workers})')

    def _undo_move(self):
        return False

    def _redo_move(self):
        return False

    def run(self):
        self._setup()

        while (True):
            self._current_player = self._players[(self._turn-1) % 2]

            self._display_current_game_state()

            if self._game_is_over():
                break

            move = self._current_player.make_move(self.board)
            
            # self.board.update_worker_position(worker, mv_d)
            # self._current_player.bu
            # # self.save_move(move)

            self._increment_turn()
        
