from .match4game import Match4Command, Match4Game, Match4State, Match4Agent
from typing import Callable
import random
import numpy as np
import math


class MinimaxNode:
	"""
		fds
  
  	"""	

	state: Match4State
	value: float
	# successors: list[tuple(Match4Node, Match4Move)]


	def __init__(self, state: Match4State):
		"""
		Stores the node's state, (heuristic) value, and a dictionary of successor nodes,
		where the keys are possible moves and the values are the successor nodes resulting from those moves

		:param  state: The state associated with this node
		:type state: State
		"""
		self.state = state
		self.value = 0.0
		self.successors = []

	def __eq__(self, other):
		return self.state == other.state and self.value == other.value and self.successors == other.successors


class MiniMaxAgent(Match4Agent):
    h_function: Callable[[Match4State, int], float]
    max_depth = 1

    def __init__(self, h, max_depth) -> None:
        super().__init__()
        self.h_function = h
        self.max_depth = max_depth

    def take_turn(self, game: Match4Game) -> Match4Command:
        S = game.get_state()
        
        root = MinimaxNode(S)
        self.apply_minimax(root)
        
        # get a list of best moves possible, choose one randomly
        best_moves: list[Match4Command] = []
        best_val = -math.inf
        for node, move in root.successors:
            if len(best_moves) == 0 or node.value > best_val:
                best_moves = [move]
                best_val = node.value
            elif node.value == best_val:
                best_moves.append(move)
        return best_moves[random.randint(0, len(best_moves)-1)]
    
    def apply_minimax(self, node: MinimaxNode, k=0, alpha=-math.inf, beta=math.inf):
        if (k == self.max_depth or node.state.terminal):
            node.value = self.h_function(node.state, self.player_id)
        else:
            # first find all legal moves
            legal_moves = [
                move for i in range(node.state.board.shape[0])
                if (move := Match4Command(column=i, player_id=node.state.current_player)) and
                Match4Game.legal_move_state(move, node.state)
            ]

            # create list of legal moves that can be created
            children = [(MinimaxNode(Match4Game.peak_command(move, node.state)), move) for move in legal_moves]
            node.successors = children
                
            if (node.state.current_player == self.player_id):
                node.value = -math.inf
                for child in node.successors:
                    node.value = max(node.value, self.apply_minimax(child[0], k + 1))
                    alpha = max(alpha, node.value)
                    if beta <= alpha:
                        break
            else:
                node.value = math.inf
                for child in node.successors:
                    node.value = min(node.value, self.apply_minimax(child[0], k + 1))
                    beta = min(beta, node.value)
                    if beta <= alpha:
                        break
        return node.value

"""

    some simple heuristic functions

"""

class ZeroH_MiniMax_Match4(MiniMaxAgent):
    def __init__(self, max_depth=2):
        super().__init__(ZeroH_MiniMax_Match4.zero_heurisitic, max_depth)
        
    def zero_heurisitic(S: Match4State, max_player: int) -> float:
        if (S.terminal):
            if (S.winner_player == max_player):
                return 100.0
            else:
                return -100.0
        return 0.0


class ThreeCountH_MiniMax_Match4(MiniMaxAgent):
    
    def __init__(self, max_depth=2):
        super().__init__(ThreeCountH_MiniMax_Match4.three_line_heuristic, max_depth)

    def three_line_heuristic(S: Match4State, max_player: int) -> float:
        if (S.terminal):
            if (S.winner_player == max_player):
                return 100.0
            else:
                return -100.0
            
        counted = 0
        counted_oponent = 0

        for i in range(Match4Game.num_cols):
            for j in range(Match4Game.num_rows):
                cur_pos = np.array([i, j])
                winner = S.board[i][j]
                if (winner == 0): continue
                for mov in [[0, 1], [1, 0], [-1, -1], [-1, 1]]:
                    mov = np.array(mov)
                    for m in range(3):
                        pos = cur_pos + mov * m
                        if (not (0 <= pos[0] < S.board.shape[0]) or not (0 <= pos[1] < S.board.shape[1])): break
                        # if (pos[0] >= S.board.shape[0] or pos[1] >= S.board.shape[1] or pos[0] < 0 or pos[1] < 0):
                        #     break
                        if (S.board[pos[0]][pos[1]] != winner):
                            break
                        if (m == 2):
                            counted += 1 if (winner == max_player) else 0
                            counted_oponent += 1 if (winner != max_player) else 0
        
        return 1.0 * counted - 1.0 * counted_oponent





