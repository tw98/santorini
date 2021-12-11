def height_score(board, player):
    return sum([board.get_building_height_of_worker(worker) for worker in player.workers])

def center_score(board, player):
    score = 0
    for worker in player.workers:
        w_r, w_c = board.get_worker_position(worker)
        # center space
        if w_r == 2 and w_c == 2:
            score += 2
        # inner ring - horizontal edges
        elif (w_r == 1 or w_r == 3) and (w_c > 0 and w_c < 4):
            score += 1
        # inner ring - vertical edges
        elif (w_c == 1 or w_c == 3) and (w_r > 0 and w_r < 4):
            score += 1
    return score

def chebyshev_distance(x1, x2, y1, y2):
    dx = abs(x1 - x2)
    dy = abs(y1 - y2)
    return dx + dy - min(dx, dy)

def distance_score(board, player):
    """ 
    Find max_distance - (sum of the minimum distance to the opponent's workers)
    EX: 8 - (min(distance Z to A, distance Y to A) + min(distance Z to B, distance Y to B))
    """
    max_distance = 8
    opp_workers = [w for w in board.get_all_workers_in_game() if w not in player.workers]
    score = 0
    for opp_worker in opp_workers:
        o_r, o_c = board.get_worker_position(opp_worker)
        distances = []
        for worker in player.workers:
            w_r, w_c = board.get_worker_position(worker)
            distance = chebyshev_distance(w_r, o_r, w_c, o_c)
            distances.append(distance)

        score += min(distances)
    return max_distance - score
    
def move_score(c1=3, c2=2, c3=1):
    move_score = c1*height_score + c2*center_score + c3*distance_score
    return move_score