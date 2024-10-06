from match4game import Match4Command, Match4Game, Match4State
from agentsABC import Match4Agent
from typing import Callable
import random

class MiniMaxAgent(Match4Agent):
    hueristic_function: Callable[[Match4State], int]
    max_depth = 1

    def __init__(self, h, max_depth) -> None:
        super().__init__()
        self.hueristic_function = h
        self.max_depth = max_depth

    def take_turn(self, game: Match4Game) -> Match4Command:
        S = game.get_state()
        

    def minimax(self, state: Match4State, depth: int) ->:

