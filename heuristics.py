'''
Define a set of heuristics to calculate the best directions for a worker to move/build.
'''

def height_score(board, workers):
    '''
    Returns the sum of the heights of the buildings a player's workers stand on.
    (It is better to get workers higher so they can try to win, but also because
    it is easier to move down than up.)
    '''
    return sum([board.get_building_height_of_worker(worker) for worker in workers])

def center_score(board, workers):
    '''
    Returns the sum of each worker's proximity to the center according to the scheme:
        center spot => 2
        ring around center => 1
        edge spots => 0
    (Having workers near the middle of the board gives more flexibility.)
    '''
    score = 0
    for worker in workers:
        w_r, w_c = board.get_worker_position(worker)
        # center space
        if w_r == 2 and w_c == 2:
            score += 2
        # inner ring
        elif (w_r > 0 and w_r < 4) and (w_c > 0 and w_c < 4):
            score += 1
    return score

def chebyshev_distance(x1, x2, y1, y2):
    dx = abs(x1 - x2)
    dy = abs(y1 - y2)
    return dx + dy - min(dx, dy)

def distance_score(board, workers):
    '''
    Returns a score to minimize the distance to the opponent's workers.
    Since higher scores are better, subtract the minimum distance from 8 (the maximum distance).
    (Having a worker near your opponents can help stop them from winning by building a dome.)
    EX: 8 - (min(distance Z to A, distance Y to A) + min(distance Z to B, distance Y to B))
    '''
    max_distance = 8
    opp_workers = [w for w in board.get_all_workers_in_game() if w not in workers]
    score = 0
    for opp_worker in opp_workers:
        opp_row, opp_col = board.get_worker_position(opp_worker)
        distances = []
        for worker in workers:
            w_row, w_col = board.get_worker_position(worker)
            distance = chebyshev_distance(w_row, opp_row, w_col, opp_col)
            distances.append(distance)
        score += min(distances)
    return max_distance - score
    
def move_score(board, workers, c1=3, c2=2, c3=1):
    h_score = height_score(board, workers)
    c_score = center_score(board, workers)
    d_score = distance_score(board, workers)
    return c1*h_score + c2*c_score + c3*d_score

