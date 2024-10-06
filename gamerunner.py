from agentsABC import Match4Agent
from match4game import Match4Game
from randomAgent import RandomMatch4Agent
from humenAgent import HumenMatch4Agent

class Gamerunner_Match4:
    game: Match4Game
    p1: Match4Agent
    p2: Match4Agent
    cur_player: Match4Agent

    def __init__(self, p1, p2):

        self.game = Match4Game()
        self.p1 = p1
        self.p1.player_id = 1
        self.p2 = p2
        self.p2.player_id = 2
        self.cur_player = p1

    def run(self):
        # game.setup()
        # game.start()
        
        self.print_state()
        while True:
            while(True):
                command = self.cur_player.take_turn(self.game)
                if(self.game.legal_move(command)):
                    break
                print("Please Input a valid move")
            self.game.apply_command(command)
            self.next_player()
            self.print_state()
            if (self.game.is_terminal()):
                print("Game Finished")
                print(f"Winner: Player {int(self.game._state.winner_player)}")
                break

    
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
    game_runner.run()



if __name__ == "__main__":
    main()


    
