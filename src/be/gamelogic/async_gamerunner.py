from .agentsABC import Match4Agent
from .match4game import Match4Game, Match4State, Match4Command
from .humenAgent import HumenMatch4Agent
from copy import deepcopy




class AsyncGamerunner_Match4:
    game: Match4Game
    p1: Match4Agent
    p2: Match4Agent
    cur_player: Match4Agent
    command_histo: list[Match4Command]
    state_histo: list[Match4State]


    def __init__(self, p1, p2):
        self.game = Match4Game()
        self.p1 = p1
        self.p1.player_id = 1
        self.p2 = p2
        self.p2.player_id = 2
        self.cur_player = p1
        self.command_histo = []
        self.state_histo = []
        self.latest_move_read = 0

    """
        start a fresh new game and start the playing process
    """
    def start(self):
        self.game.setup()
        if (not isinstance(self.cur_player, HumenMatch4Agent)): self.apply_move(0, 1, is_bot=True)

    def apply_move(self, move: int, player_id: int, is_bot=False):
        if (is_bot):
            command = self.cur_player.take_turn(self.game)
        else:
            command = Match4Command()
            command.column = move - 1
            command.player_id = player_id
        self.game.apply_command(command)
        self.command_histo.append(deepcopy(command))
        self.state_histo.append(deepcopy(self.game.get_state()))
        self.cur_player = self.p2 if (self.cur_player is self.p1) else self.p1 
        if (not isinstance(self.cur_player, HumenMatch4Agent)): self.apply_move(0, 1, is_bot=True)
        
    def see_state(self) -> tuple[Match4State, Match4Command]:
        if (self.latest_move_read < len(self.state_histo)):
            raise IndexError(" read moves before the move was made")
        self.latest_move_read += 1
        return self.state_histo[self.latest_move_read - 1], self.command_histo[self.latest_move_read - 1]
        
    
    