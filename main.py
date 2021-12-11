import argparse
from game_engine import GameEngine

parser = argparse.ArgumentParser()
parser.add_argument("p1_type", nargs='?', default='human')
parser.add_argument("p2_type", nargs='?', default='human')
parser.add_argument("undo_redo", nargs='?', default='off')
parser.add_argument("enable_score", nargs='?',default='off')

if __name__ == "__main__":
    args = parser.parse_args()

    print(args)

    # check args here?

    env = GameEngine(args.p1_type, args.p2_type, args.undo_redo, args.enable_score)
    env.run()