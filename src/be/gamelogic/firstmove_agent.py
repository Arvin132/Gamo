from .match4game import Match4Command, Match4Game, Match4State
from .agentsABC import Match4Agent
import random

"""
    FirstMoveMatch4Agent:
        agents takes the first legal action avaible at each turn

"""

class FirstMoveMatch4Agent(Match4Agent):
    def take_turn(self, game: Match4Game) -> Match4Command:
        S = game.get_state()
        command_pool = []
        for i in range(S.board.shape[0]):
            command = Match4Command()
            command.column = i
            command.player_id = self.player_id
            if(game.legal_move(command)):
                command_pool.append(command)

        return command_pool[0]
