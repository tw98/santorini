import utils

class Caretaker:
    def __init__(self, board) -> None:
        self._history = []
        self._redo_stack = []
        self._board = board
    
    def backup(self, worker, move_dir, build_dir):
        self._history.append((worker, move_dir, build_dir))
        self._redo_stack = []

    def undo(self):
        if self._history:
            worker, move_dir, build_dir = self._history.pop()

            reverse_move = utils.reverse_direction(move_dir)
            reverse_build = utils.reverse_direction(build_dir)
            self._board.decrement_building_height(worker, reverse_build)
            self._board.move_worker(worker, reverse_move)

            self._redo_stack.append((worker, move_dir, build_dir))
            return True
        return False

    def redo(self):
        if self._redo_stack:
            worker, move_dir, build_dir = self._redo_stack.pop()
            self._board.move_worker(worker, move_dir)
            self._board.increment_building_height(worker, build_dir)

            self._history.append((worker, move_dir, build_dir))
            return True
        return False