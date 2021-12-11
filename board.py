class Board:
    def __init__(self):
        self.n_rows = 5
        self.n_cols = 5
        self._board = []
        for row in range(self.n_rows):
            row = []
            for col in range(self.n_cols):
                row.append([0, None])
            self._board.append(row)

        self._worker_positions = {}

        self.direction_vectors = {
            'n': (-1, 0),
            'ne': (-1, 1),
            'e': (0, 1),
            'se': (1, 1),
            's': (1, 0),
            'sw': (1, -1),
            'w': (0, -1),
            'nw': (-1, -1),
        }

    def get_all_workers_in_game(self):
        return list(self._worker_positions.keys())

    def get_worker_position(self, worker):
        return self._worker_positions[worker]

    def set_worker_position(self, worker, row, col):
        if worker not in self._worker_positions:
            # initialize
            self._board[row][col][1] = worker
            self._worker_positions[worker] = (row, col)
        else:
            # normal update: 
            # free current position
            cur_row, cur_col = self.get_worker_position(worker)
            self._board[cur_row][cur_col][1] = None
            # set new position
            self._board[cur_row+row][cur_col+col][1] = worker
            self._worker_positions[worker] = (cur_row+row, cur_col+col)

    def check_game_winning_position(self):
        for worker in self._worker_positions:
            row, col = self._worker_positions[worker]
            if self._board[row][col][0] >= 3:
                return worker
        return None

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

    def is_valid_move_direction(self, d, worker):
        if d in self.get_valid_moves(worker):
            return True
        return False

    def is_valid_build_direction(self, d, worker):
        if d in self.get_valid_builds(worker):
            return True
        return False

    def get_valid_moves(self, worker):
        valid_moves = []
        cur_row, cur_col = self.get_worker_position(worker)
        cur_height = self._board[cur_row][cur_col][0]
        
        for d in self.direction_vectors:
            next_row = cur_row + self.direction_vectors[d][0]
            next_col = cur_col + self.direction_vectors[d][1]

            # check within board dimensionality
            if next_row < 0 or next_row >= self.n_rows:
                continue
            if next_col < 0 or next_col >= self.n_cols:
                continue

            # check height constraints
            next_height = self._board[next_row][next_col][0]
            if next_height > cur_height+1:
                continue

            # check worker occupancy
            next_occupancy = self._board[next_row][next_col][1]
            if next_occupancy is not None:
                continue

            # check dome existence
            if next_height == 4:
                continue
            
            # passed all checks, valid direction
            valid_moves.append(d)
        
        return valid_moves

    def get_valid_builds(self, worker):
        valid_builds = []
        cur_row, cur_col = self.get_worker_position(worker)
        
        for d in self.direction_vectors:
            next_row = cur_row + self.direction_vectors[d][0]
            next_col = cur_col + self.direction_vectors[d][1]

            # check within board dimensionality
            if next_row < 0 or next_row >= self.n_rows:
                continue
            if next_col < 0 or next_col >= self.n_cols:
                continue

            # check worker occupancy
            next_occupancy = self._board[next_row][next_col][1]
            if next_occupancy is not None:
                continue
            
            # check dome existence
            next_height = self._board[next_row][next_col][0]
            if next_height >= 4:
                continue

            valid_builds.append(d)
        return valid_builds

    def move_worker(self, worker, direction):
        row = self.direction_vectors[direction][0]
        col = self.direction_vectors[direction][1]

        self.set_worker_position(worker, row, col)

    def increment_building_height(self, worker, direction):
        cur_row, cur_col = self.get_worker_position(worker)
        row = self.direction_vectors[direction][0]
        col = self.direction_vectors[direction][1]

        self._board[cur_row+row][cur_col+col][0] += 1

    def decrement_building_height(self, worker, direction):
        cur_row, cur_col = self.get_worker_position(worker)
        row = self.direction_vectors[direction][0]
        col = self.direction_vectors[direction][1]

        self._board[cur_row+row][cur_col+col][0] -= 1

    def get_building_height_of_worker(self, worker):
        cur_row, cur_col = self.get_worker_position(worker)
        return self._board[cur_row][cur_col][0]