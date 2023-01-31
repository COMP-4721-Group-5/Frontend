class Player:
    """Keeps track of all player specific data

    Contains all player data, 

    Attributes:
        hand: list of tiles representing the player's hand

    """
    hand = {}
    score = 0

    """Removes the designated tile from players hand, used for play and discard actions
    
    Args:
        index: index of the tile to be removed

    Returns:
        true: if the remove was succesful
        false: if not
    """
    def play_tile(index):
        pass
    
