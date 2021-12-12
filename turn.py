class Turn:
    def __init__(self, turn_no, turn_type, worker, move, build):
        self.turn_no = turn_no
        self.turn_type = turn_type
        self.worker = worker
        self.move = move # direction
        self.build = build # direction