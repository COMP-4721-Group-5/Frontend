from typing import List

from .internal_structures import Tile

class Player:
    """Keeps track of all player specific data

    Contains all player data, 

    Attributes:
        hand: list of tiles representing the player's hand

    """
    hand: List[Tile]
    score = 0
    
    def update_hand(self, hand: List[Tile]):
        self.hand = hand


    def play_tile(self, index: int):
        """Removes a given tile from the player's hand

        Args:
            index: index of the tile to be removed
        """
        played = self.hand[index]
        self.hand[index] = None
        return played
