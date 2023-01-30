class Gamerules:
    """A representation of the game's logic

    Responsible for ensuring consistency with game logic and contains methods for altering the board model
    as per legal moves by the game's rules.
    """

    def verify_move(self, move):
        """Verifies the most recent move

        Ensures that a given move is legal by game rules.

        Args: 
            move: A list of tuples containing a tile and it's given indices 
                to represent the most recent move. For example:

                {(Tile 1, x cord 1, y cord 1), (Tile 2, x cord 2, y cord 2)...}
        
        Returns: 
            Boolean corresponding to the validity of the move, true if the move is
                determined to be legal, false if it is not.
        """

    def register_move(self, move):
        """Registers a given move.

        Updates the board to include the most recent move.

        Args: 
            move: A list of tuples containing a tile and it's given indices 
                to represent the most recent move. For example:

                {(Tile 1, x cord 1, y cord 1), (Tile 2, x cord 2, y cord 2)...}
        
        Returns:
            Boolean corresponding to if the move was succesfully registered.
            
        """ 
    def score_move(self, move):
        """Scores a given move.

        Args:
            move: A list of tuples containing a tile and it's given indices 
                to represent the most recent move. For example:

                {(Tile 1, x cord 1, y cord 1), (Tile 2, x cord 2, y cord 2)...}

        Returns: 
            Integer represent of the score of the move.
        """