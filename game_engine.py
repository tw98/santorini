from players import PlayerFactory
from board import Board
import heuristics as h

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
        self.undo_redo = False
        if undo_redo == 'on':
            self.undo_redo = True

        self.enable_score = False
        if enable_score == 'on':
            self.enable_score = True

    def set_starting_postion(self):
        player1_worker1 = self._players[0].workers[0]
        self.board.set_worker_position(player1_worker1, 3, 1)
        player1_worker2 = self._players[0].workers[1]
        self.board.set_worker_position(player1_worker2, 1, 3)
        player2_worker1 = self._players[1].workers[0]
        self.board.set_worker_position(player2_worker1, 1, 1)
        player2_worker2 = self._players[1].workers[1]
        self.board.set_worker_position(player2_worker2, 3, 3)

    def increment_turn(self):
        self._turn += 1

    def _game_is_over(self):
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

    def display_current_game_state(self):
        self.board.display()
        color = self._current_player.color
        workers = ''.join(self._current_player.workers)

        output = f'Turn: {self._turn}, {color} ({workers})'

        if self.enable_score:
            height_score = h.height_score(self.board, self._current_player)
            center_score = h.center_score(self.board, self._current_player)
            dist_score = h.distance_score(self.board, self._current_player)
            output += f', ({height_score}, {center_score}, {dist_score})'
        print(output)

    def _undo_move(self):
        return False

    def run(self):
        self.set_starting_postion()

        while (True):
            self._current_player = self._players[(self._turn-1) % 2]

            self.display_current_game_state()

            if self._game_is_over():
                break

            move = self._current_player.make_move(self.board)
            # self.board.update_worker_position(worker, mv_d)
            # self._current_player.bu
            # # self.save_move(move)

            self.increment_turn()
        

