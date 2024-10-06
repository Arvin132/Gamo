import abc
from match4game import Match4Command, Match4Game

class Match4Agent(abc.ABC):
    player_id: int

    @abc.abstractmethod
    def take_turn(self, game: Match4Game)-> Match4Command:
        """
        takes a single turn
        """

