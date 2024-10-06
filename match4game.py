from copy import deepcopy
import numpy as np




class Match4State:
    board: np.ndarray
    terminal: bool
    current_player: int
    winner_player: int



class Match4Command():
    column: int
    player_id: int
 
class Match4Game:
    _state: Match4State

    def __init__(self) -> None:
        self._state = Match4State
        self._state.board = np.zeros((8, 8))
        self._state.terminal = False
        self._state.current_player = 1
        self._state.winner_player = -10 # dummy values

    def get_state(self) -> Match4State:
        return deepcopy(self._state)
    
    def apply_command(self, command: Match4Command) -> bool:
        row = self._state.board.shape[0] - 1
        while(self._state.board[row][command.column] != 0):
            row -= 1
            if (row < 0):
                return False
        self._state.board[row][command.column] = command.player_id
        self.check_for_terminal()
        return True
    
    def check_for_terminal(self) -> int:
        return self.check_for_terminal_for_state(self._state)
    
    def check_for_terminal_for_state(self, state: Match4State) -> int:
        for i in range(8):
            for j in range(8):
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
