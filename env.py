from players import PlayerFactory
from board import Board
import sys

class GameEngine:
    def __init__(self, player1_type, player2_type, redo, enable_score) -> None:
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
        return False

    def display_current_game_state(self):
        self.board.display()
        color = self._current_player.color
        workers = ''.join(self._current_player.workers)
        print(f'Turn: {self._turn}, {color} ({workers})')

    def _undo_move(self):
        return False

    def run(self):
        self.set_starting_postion()

        while (not self._game_is_over()):
            # self._undo_move():
            
            self._current_player = self._players[(self._turn-1) % 2]

            self.display_current_game_state()

            move = self._current_player.make_move(self.board)
            # self.board.update_worker_position(worker, mv_d)
            # self._current_player.bu
            # # self.save_move(move)

            self.increment_turn()
            
if __name__ == "__main__":
    player1_type = 'human'
    player2_type = 'human'
    redo = 'off'
    enable_score = 'off'

    env = GameEngine(player1_type, player2_type, redo, enable_score)
    env.run()

