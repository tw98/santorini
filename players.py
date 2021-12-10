import heuristics


# @abstract Player Class Template
class Player:
    def __init__(self, workers, color, type) -> None:
        self.__workers = workers
        pass

    def has_worker(self, worker):
        return worker in self.__workers

    def move():
        pass

    def build():
        pass


class PlayerFactory():
    def __init__(self) -> None:
        pass

    def create_player():
        pass

class HumanPlayer(Player):
    def __init__(self) -> None:
        pass

class RandomPlayer(Player):
    def __init__(self) -> None:
        pass

class HeurisitcsPlayer(Player):
    def __init__(self) -> None:
        pass