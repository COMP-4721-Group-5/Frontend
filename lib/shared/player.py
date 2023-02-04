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
    __score = 0
    
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

    def __getitem__(self, key: int):
        return self.__hand[key]
    
    def __setitem__(self, key: int, value: Tile):
        self.__hand[key] = value

