class Board:
    def __init__(self):
        N_ROWS = 5
        N_COLS = 5
        self._board = []
        for row in range(N_ROWS):
            row = []
            for col in range(N_COLS):
                row.append([0, None])
            self._board.append(row)

    def set_worker_position(self, worker, row, col):
        self._board[row][col][1] = worker

    def display(self):
        separator = '+--+--+--+--+--+'
        print(separator)
        for row in self._board:
            row_str = []
            for elt in row:
                elt_str = '|'
                elt_str += str(elt[0])
                if elt[1]:
                    elt_str += elt[1]
                else:
                    elt_str += ' '
                row_str.append(elt_str)
            print(''.join(row_str) + '|')
            print(separator)

    # only Human Player
    def is_valid_move_direction(self, d, worker):
        return True

    def is_valid_build_direction(self, d, worker):
        return True

    # AI player
    def get_valid_moves(self, worker):
        pass

class Move:
    def __init__(self) -> None:
        self.worker = None
        self.move_direction = None
        self.build_direction = None