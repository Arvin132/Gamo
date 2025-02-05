from copy import deepcopy
import numpy as np
import json
import abc





class Match4State:
    board: np.ndarray
    terminal: bool
    current_player: int
    winner_player: int

    def __eq__(self, other):
        return self.board == other.board and self.terminal == other.terminal and self.current_player == other.current_player \
                and self.winner_player == other.winner_player



class Match4Command():
    column: int
    player_id: int
    
    def to_dict(self):
        return {"column": self.column,
                "player_id" : self.player_id}
    def from_dict(given):
        command = Match4Command()
        command.column = given["column"]
        command.player_id = given["player_id"]
        return command
    
    def __init__(self, column=-10, player_id=10) -> None:
        self.column = column
        self.player_id = player_id

class Match4Game:
    _state: Match4State
    tie_value = 3
    num_cols = 8
    num_rows = 8

    def __init__(self) -> None:
       self.setup()  

    def setup(self) -> None:
        self._state = Match4State()
        self._state.board = np.zeros((self.num_rows, self.num_cols))
        self._state.terminal = False
        self._state.current_player = 1
        self._state.winner_player = -10 # dummy values


    def get_state(self) -> Match4State:
        return deepcopy(self._state)
    
    def apply_command(self, command: Match4Command):
        # checks if the given command is a correct command
        if (not isinstance(command, Match4Command)):
            raise TypeError("Gamerunner_Match4 said: Expected a Match4Command from given Match4Agent")
        if (command.player_id != self._state.current_player):
            raise ValueError(f"Gamerunner_Match4 said: Expected a Match4Command for current player {self._state.current_player}, got command for player {command.player_id}")
        if (not self.legal_move(command)):
            raise ValueError("Gamerunner_Match4 said: Expected a legal Match4Command, got an illegal one !!")
        

        row = self._state.board.shape[0] - 1
        while(self._state.board[row][command.column] != 0):
            row -= 1
            if (row < 0):
                raise IndexError(f"Acess to invalid row; row = {row}")
        self._state.board[row][command.column] = command.player_id
        self._state.current_player = 1 if self._state.current_player == 2 else 2
        self.check_for_terminal()
        return True
    
    def peak_command(command: Match4Command, state: Match4State) -> Match4State:
        retVal = deepcopy(state)
        row = retVal.board.shape[0] - 1
        while(retVal.board[row][command.column] != 0):
            row -= 1
        retVal.board[row][command.column] = command.player_id
        retVal.current_player = 2 if state.current_player == 1 else 1
        Match4Game.check_for_terminal_for_state(retVal)
        return retVal
    
    def check_for_terminal(self) -> int:
        return Match4Game.check_for_terminal_for_state(self._state)
    
    def check_for_terminal_for_state(state: Match4State) -> int:
        for i in range(Match4Game.num_cols):
            for j in range(Match4Game.num_rows):
                cur_pos = np.array([i, j])
                winner = int(state.board[i][j])
                if (winner == 0): continue
                for mov in [[0, 1], [1, 0], [-1, -1], [-1, 1]]:
                    mov = np.array(mov)
                    for m in range(4):
                        pos = cur_pos + mov * m
                        if (pos[0] >= state.board.shape[0] or pos[1] >= state.board.shape[1] or pos[0] < 0 or pos[1] < 0):
                            break
                        if (state.board[pos[0]][pos[1]] != winner):
                            break
                        if (m == 3):
                            state.winner_player = int(winner)
                            state.terminal = True
                            return winner
                        
        # if no winner check for a tie:
        for i in range(Match4Game.num_cols):
            if (state.board[0][i] == 0):
                break
            if (i == 7):
                state.terminal = True
                state.winner_player = Match4Game.tie_value
                return Match4Game.tie_value
        return 0
    
    def legal_move(self, command: Match4Command) -> bool:
        return Match4Game.legal_move_state(command, self._state)
        
    def legal_move_state(command: Match4Command, state: Match4State) -> bool:
        try:
            if(state.board[0][command.column] != 0):
                return False
            return True
        except:
            return False
    
    def is_terminal(self) -> bool:
        return self._state.terminal
    
    def to_dict(self) -> dict:
        return {
            "board": self._state.board.tolist(), 
            "terminal": self._state.terminal,
            "current_player": self._state.current_player,
            "winner_player": self._state.winner_player
        }
    def from_dict(given):
        game = Match4Game()
        game._state.board = np.array(given["board"], dtype=int)
        game._state.terminal = given["terminal"]
        game._state.current_player = given["current_player"]
        game._state.winner_player = given["winner_player"]
        return game
    def to_json(self) -> str:
        return json.dumps(self.to_dict())

    def from_json(self, json_str: str):
        state_dict = json.loads(json_str)
        self._state.board = np.array(state_dict['board'])  # Convert list back to NumPy array
        self._state.terminal = state_dict['terminal']
        self._state.current_player = state_dict['current_player']
        self._state.winner_player = state_dict['winner_player']



"""
    Match4Agent:
        abstract base class designed to create agents to play Match4Games.
        at each turn the game will call the method take_turn() to determine the next move of the agent

    How to create your own agent:

        **mandatory** : override take_turn(game) method.
            1- make sure that you return a Match4Command
            2- make sure that you return a "legal" command. this can be checked using the game.legal_move(command) method
            3- make sure that the command that you return has the same player_id equal to your agents
        
        optional: override the learn() method to pre-train a model if you wish to for the purpose of the Agent!
            1- make sure that if you write a new Constructor for your class you call super().__init__()
"""

class Match4Agent(abc.ABC):
    player_id: int
    def __init__(self) -> None:
        self.learn()
        
    @abc.abstractmethod
    def take_turn(self, game: Match4Game)-> Match4Command:
        None
    
    def learn(self):
        None

