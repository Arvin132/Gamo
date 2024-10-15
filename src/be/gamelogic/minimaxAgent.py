from .match4game import Match4Command, Match4Game, Match4State
from .agentsABC import Match4Agent
from typing import Callable
import random
import heapq


class MinimaxNode:
    """
    One node in the Minimax search tree.
    """

	state: Match4State
	value: int
	# successors


    def __init__(self, state: State):
        """
        Stores the node's state, (heuristic) value, and a dictionary of successor nodes,
        where the keys are possible moves and the values are the successor nodes resulting from those moves

        :param  state: The state associated with this node
        :type state: State
        """
        self.state = state
        self.value = 0
        self.successors = {}

    def __eq__(self, other):
        return self.state == other.state and self.value == other.value and self.successors == other.successors


class MiniMaxAgent(Match4Agent):
    h_function: Callable[[Match4State, int], int]
    max_depth = 1

    def __init__(self, h, max_depth) -> None:
        super().__init__()
        self.h_function = h
        self.max_depth = max_depth

    def take_turn(self, game: Match4Game) -> Match4Command:
        S = game.get_state()
		moves = apply_minimax()
		root = MinimaxNode(S)
        apply_minimax(game, root)
        best_moves = []
        for move in root.successors.keys():
            if len(best_moves) == 0 or root.successors[move].value > root.successors[best_moves[0]].value:
                best_moves = [move]
            elif root.successors[move].value == root.successors[best_moves[0]].value:
                best_moves.append(move)
		retVal = Match4Command()
		retVal.column = best_moves[randint(0, len(best_moves)-1)]
		retVal.player_id = self.player_id
        return retVal

    def apply_minimax(self, game: Match4Game, node: MinimaxNode, k=0) -> list[tuple(Match4Command, int)]:
        # if (k == max_depth or S.terminal):
		# 	return [(Match4Command(), h_function(S, self.player_id))]

		

		
		# best_moves = []

		# for command in legal_moves:
		# 	S_next = game.peak_command(command, S)
		# 	results = apply_minimax(game, S_next, k + 1)
		# 	if (len(best_moves) == 0 or results[0][1] > best_moves[0])

		if (k == max_depth or S.terminal):
        	node.value = self.h_function(node.state)
		else:
			# create childs of node
			children = {}

			# find legal moves
			legal_moves = []
			for i in range(S.board.shape[0]):
				command = Match4Command()
				command.column = i
				command.player_id = self.player_id
				if (game.legal_move(command)):
					legal_moves.append(command)
			

			for move in legal_moves:
				res = node
			for i in range(game.num_cols):
				res = node.state.peek_next_board(i)
				if (res != None):
					children[i] = MinimaxNode(State(node.state.num_cols, node.state.num_rows, other_player, res))
			node.successors = children



			if (cur_player == max_role):
				node.value = -math.inf
				for child in node.successors.values():
					node.value = max(node.value, minimax(child, depth - 1, max_role, heuristic_fn))
			else:
				node.value = math.inf
				for child in node.successors.values():
					node.value = min(node.value, minimax(child, depth - 1, max_role, heuristic_fn))

    	return node.value


"""

    some simple heuristic functions

"""


def zero_heurisitic(S: Match4State, max_player: int) -> int:
	"""
		Heuristic function  for usage on Match4State

			in case of terminal state returns 100 for win and -100 for loss. otherwise returns 0 always
	"""

	if (S.terminal):
		if (S.winner_player == max_player):
			return 100
		else:
			return -100
	return 0
