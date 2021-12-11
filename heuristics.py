def height_score(board, player):
    return sum([board.get_building_height_of_worker(worker) for worker in player.workers])

def center_score(board, worker):
    pass

def distance_score(board, workers):
    pass

def move_score(c1=3, c2=2, c3=1):
    move_score = c1*height_score + c2*center_score + c3*distance_score
    return move_score
