NEXT = 'next'
UNDO = 'undo'
REDO = 'redo'

DIRECTIONS = ['n', 'ne', 'e', 'se', 's', 'sw', 'w', 'nw']

REVERSE_DIRECTIONS = {
    'n': 's',
    'ne': 'sw',
    'e': 'w', 
    'se': 'nw',
    's': 'n',
    'sw': 'ne',
    'w': 'e',
    'nw': 'se'
}

def reverse_direction(direction):
    return REVERSE_DIRECTIONS[direction]
