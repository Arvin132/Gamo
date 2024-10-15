from .match4game import Match4Command, Match4Game, Match4State
from .agentsABC import Match4Agent


"""
    HumenMatch4Agent:
        match 4 agent created to use CL as input method for the player
"""


class HumenMatch4Agent(Match4Agent):
    def take_turn(self, game: Match4Game) -> Match4Command:
        print(f"Humen Player {self.player_id}: Input the row you want to put the token")
        column = int(input())
        command = Match4Command()
        command.column = column
        command.player_id = self.player_id
        if (not game.legal_move(command)):
            print("Please Input a valid move")
            return self.take_turn(game)
        return command
