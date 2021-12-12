'''
Define a set of heuristics to calculate the best directions for a worker to move/build.
'''

def height_score(hypothetical_worker, hypothetical_move, board, workers):
    '''
    Returns the sum of the heights of the buildings a player's workers stand on.
    (It is better to get workers higher so they can try to win, but also because
    it is easier to move down than up.)
    '''
    h_score = 0
    for worker in workers:
        if worker == hypothetical_worker:
            h_score += board.get_building_height_in_direction(worker, hypothetical_move)
        else:
            h_score += board.get_building_height_of_worker(worker)
    return h_score

def center_score(hypothetical_worker, hypothetical_move, board, workers):
    '''
    Returns the sum of each worker's proximity to the center according to the scheme:
        center spot => 2
        ring around center => 1
        edge spots => 0
    (Having workers near the middle of the board gives more flexibility.)
    '''
    c_score = 0
    for worker in workers:
        if worker == hypothetical_worker:
            c_score += board.get_center_proximity_in_direction(worker, hypothetical_move)
        else:
            c_score += board.get_center_proximity_of_worker(worker)
    return c_score

def distance_score(hypothetical_worker, hypothetical_move, board, workers):
    '''
    Returns a score to minimize the minimum distance to the opponent's workers.
    Since higher scores are better, subtract the minimum distance from 8 (the maximum distance).
    (Having a worker near your opponents can help stop them from winning by building a dome.)
    '''

    pass

def move_score(hypothetical_worker, hypothetical_move, board, workers, c1=3, c2=2, c3=1):
    h_score = height_score(hypothetical_worker, hypothetical_move, board, workers)
    c_score = center_score(board, player)
    d_score = distance_score(board, player)
    return c1*h_score + c2*c_score + c3*d_score
