from .match4game import Match4Command, Match4Game, Match4State
from .agentsABC import Match4Agent
from typing import Callable
import random
import heapq
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
    
    def apply_minimax(self, node: MinimaxNode, k=0):
        if (k == self.max_depth or node.state.terminal):
            node.value = self.h_function(node.state, self.player_id)
        else:
            # first find all legal moves
            legal_moves = []
            for i in range(node.state.board.shape[0]):
                command = Match4Command()
                command.column = i
                command.player_id = node.state.current_player
                if (Match4Game.legal_move_state(command, node.state)):
                    legal_moves.append(command)
            # create list of legal moves that can be created
            children = []
            for move in legal_moves:
                res = Match4Game.peak_command(move, node.state)
                children.append((MinimaxNode(res), move))
            node.successors = children
                
            if (node.state.current_player == self.player_id):
                node.value = -math.inf
                for child in node.successors:
                    node.value = max(node.value, self.apply_minimax(child[0], k + 1))
            else:
                node.value = math.inf
                for child in node.successors:
                    node.value = min(node.value, self.apply_minimax(child[0], k + 1))
        return node.value

"""

    some simple heuristic functions

"""

class ZeroH_MiniMax_Match4(MiniMaxAgent):
    def __init__(self):
        super().__init__(ZeroH_MiniMax_Match4.zero_heurisitic, 2)
        
    def zero_heurisitic(S: Match4State, max_player: int) -> float:
        if (S.terminal):
            if (S.winner_player == max_player):
                return 100.0
            else:
                return -100.0
        return 0.0




