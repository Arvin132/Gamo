from copy import deepcopy
import numpy as np
import json



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
    
    def apply_command(self, command: Match4Command) -> bool:

        
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
                return False
        self._state.board[row][command.column] = command.player_id
        self._state.current_player = 1 if self._state.current_player == 2 else 2
        self.check_for_terminal()
        return True
    
    def check_for_terminal(self) -> int:
        return self.check_for_terminal_for_state(self._state)
    
    def check_for_terminal_for_state(self, state: Match4State) -> int:
        for i in range(self.num_cols):
            for j in range(self.num_rows):
                cur_pos = np.array([i, j])
                winner = state.board[i][j]
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
                            state.winner_player = winner
                            state.terminal = True
                            return winner
                        
        # if no winner check for a tie:
        for i in range(self.num_cols):
            if (state.board[0][i] == 0):
                break
            if (i == 7):
                state.terminal = True
                state.winner_player = self.tie_value
                return self.tie_value
        return 0
    
    def legal_move(self, command: Match4Command) -> bool:
        try:
            if(self._state.board[0][command.column] != 0):
                return False
            return True
        except:
            return False
        
    def peak_command(self, command: Match4Command, state: Match4State) -> Match4State:
        row = state.board.shape[0] - 1
        while(state.board[row][command.column] != 0):
            row -= 1
            if (row < 0):
                return False
        state.board[row][command.column] = command.player_id
        self.check_for_terminal_for_state(state)
        return deepcopy(state)
        
    
    def is_terminal(self) -> bool:
        return self._state.terminal
    
    def to_dict(self) -> dict:
        return {
            "board": self._state.board.tolist(), 
            "terminal": self._state.terminal,
            "current_player": self._state.current_player,
            "winner_player": self._state.winner_player
        }
    def to_json(self) -> str:
        return json.dumps(self.to_dict())

    def from_json(self, json_str: str):
        state_dict = json.loads(json_str)
        self._state.board = np.array(state_dict['board'])  # Convert list back to NumPy array
        self._state.terminal = state_dict['terminal']
        self._state.current_player = state_dict['current_player']
        self._state.winner_player = state_dict['winner_player']
