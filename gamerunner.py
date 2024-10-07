from agentsABC import Match4Agent
from match4game import Match4Game, Match4State, Match4Command
from randomAgent import RandomMatch4Agent
from humenAgent import HumenMatch4Agent
from copy import deepcopy



"""
            this file includes a main file for running and testing the game runner class



    Gamerunner_Match4: class designed to run match 4 game given 2 different Agents

    ctor: Gamerunner_Match4(Match4Agent p1, Match4Agent)

    - use Gamerunner_Match4.run() to start a new game
    
    - use Gamerunner_Match4.command_histo to view the history of command since the game started

    - use Gamerunner_Match4.p1 and .p2 to change the agent after the crea

"""
class Gamerunner_Match4:
    game: Match4Game
    p1: Match4Agent
    p2: Match4Agent
    cur_player: Match4Agent
    command_histo: list[Match4State]


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
    def run(self, vebose=False):
        self.game.setup()
        
        if (vebose): self.print_state()
        while True:
            command = self.cur_player.take_turn(self.game)
            
            # checks if the given command is a correct command
            if (command is not Match4Command):
                raise TypeError("Gamerunner_Match4 said: Expected a Match4Command from given Match4Agent")
            if (command.player_id != self.cur_player):
                raise ValueError(f"Gamerunner_Match4 said: Expected a Match4Command for current player {self.cur_player}, got command for player {command.player_id}")
            if (not self.game.legal_move(command)):
                raise ValueError("Gamerunner_Match4 said: Expected a legal Match4Command, got an illegal one !!")
            

            self.game.apply_command(command)
            self.command_histo.append(deepcopy(command))
            self.next_player()
            if (vebose): self.print_state()
            if (self.game.is_terminal()):
                print("Game Finished")
                if (self.game._state.winner_player == self.game.tie_value):
                    print("Tie !!")
                else:
                    print(f"Winner: Player {int(self.game._state.winner_player)}")
                break

    """
        method used to change to next player
    """
    def next_player(self):
        if (self.cur_player is self.p1):
            self.cur_player = self.p2
        else:
            self.cur_player = self.p1

    
    def print_state(self):
        state = self.game.get_state()
        for row in state.board:
            for cell in row:
                if (cell == 0):
                    print("_", end=" ")
                elif(cell == 1):
                    print("0", end=" ")
                elif(cell == 2):
                    print("X", end= " ")
                else:
                    raise ValueError(" Unknown value for the cell in match4game")
            print("")
        print()
                     

def main():
    game_runner = Gamerunner_Match4(HumenMatch4Agent(), RandomMatch4Agent())
    game_runner.run(vebose=True)



if __name__ == "__main__":
    main()


    
