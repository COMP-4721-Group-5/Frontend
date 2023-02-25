from typing import List

from .internal_structures import Tile


class Player:
    """Keeps track of all player specific data

    Contains all player data, 

    Attributes:
        hand: list of tiles representing the player's hand
        score: keeps trick of player's score

    """
    __hand: List[Tile]
    __score: int

    def __init__(self) -> None:
        self.__hand = [None] * 6
        self.__score = 0

    def update_hand(self, hand: List[Tile]):
        """Updates the hand
        
        Args:
            hand: List of tiles to represent the player's hand
        """
        self.__hand = hand

    def play_tile(self, index: int):
        """Removes a given tile from the player's hand

        Args:
            index: index of the tile to be removed
        
        Returns:
            The tile that was removed from hand
        """
        played = self.__hand[index]
        self.__hand[index] = None
        return played

    def get_hand(self):
        return self.__hand

    def __getitem__(self, key: int):
        return self.__hand[key]

    def __setitem__(self, key: int, value: Tile):
        self.__hand[key] = value

    @property
    def score(self):
        return self.__score
    
    @score.setter
    def score(self, new_score: int):
        if isinstance(new_score, int):
            if new_score < 0:
                raise ValueError('Invalid score: %d (negative)' %(new_score))
            self.__score = new_score
        else:
            raise TypeError('Invalid type')
