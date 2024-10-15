import abc
from .match4game import Match4Command, Match4Game

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

