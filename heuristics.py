def height_score():
    pass

def center_score():
    pass

def distance_score():
    pass

def move_score(c1=3, c2=2, c3=1):
    move_score = c1*height_score + c2*center_score + c3*distance_score
    return move_score
