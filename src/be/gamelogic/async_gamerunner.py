from .match4game import Match4Game, Match4State, Match4Command, Match4Agent
from copy import deepcopy

class AsyncGamerunner_Match4:
    game: Match4Game
    p1: Match4Agent
    p2: Match4Agent
    cur_player: Match4Agent
    command_histo: list[Match4Command]


    def __init__(self, p1, p2):
        self.game = Match4Game()
        self.p1 = p1
        self.p1.player_id = 1
        self.p2 = p2
        self.p2.player_id = 2
        self.cur_player = p1
        self.command_histo = []

    """
        start a fresh new game and start the playing process
    """
    def start(self):
        self.game.setup()

    def apply_move(self, move: int, player_id: int, is_bot=False):
        if (is_bot):
            command = self.cur_player.take_turn(self.game)
        else:
            command = Match4Command()
            command.column = move - 1
            command.player_id = player_id
        self.game.apply_command(command)
        self.command_histo.append(deepcopy(command))
        self.cur_player = self.p2 if (self.cur_player is self.p1) else self.p1 
        
    def to_dict(self):
        return {
            "state" : self.game.to_dict(),
            "moves": [move.to_dict() for move in self.command_histo] 
        }
    
    def from_dict(self, given: dict):
        self.game = Match4Game.from_dict(given["state"])
        self.command_histo = [Match4Command.from_dict(move) for move in given["moves"]]
        pass
    
    