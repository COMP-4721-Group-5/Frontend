from .internal_structures import Board, Placement


class Gamerules:
    """A representation of the game's logic

    Responsible for ensuring consistency with game logic and contains methods for altering the board model
    as per legal moves by the game's rules.

    Attributes:
        board: Stores the current game board
    """
    __board: Board

    def update_board(self, board: Board):
        self.__board = board

    def verify_move(self, move):
        """Verifies the most recent move

        Ensures that a given move is legal by game rules.

        Args: 
            move: A list of placements containing a tile and it's given indices 
                to represent the most recent move. For example:

                {(Tile 1, x cord 1, y cord 1), (Tile 2, x cord 2, y cord 2)...}
        
        Returns: 
            A boolean list corresponding to the validity of the move, true if the move is
                determined to be legal, false if it is not.
        """
        validPlacements = {}
        pass

    def get_lines(self, placement: Placement):
        """Check which lines a given placement could be a part of

        Interated through the board from the placement data to see what valid lines configurations
        could be made.

        Args:
            placement: placement data of the tile

        Returns:
            A list of possible lines in form of a list of tiles for ex:
                {Line:(Tile: red, circle, Tile: red, square, Tile: red, star), Line:(Tile: green, square, Tile: red, square)}
            max line length is 6
        """

        pass

    def verify_placement(self, placement: Placement) -> bool:
        """Verifies placement of a single tile on the board

        Checks to make sure a given placement is a valid move.

        Args:
            placement: placement to verify
        Return:
            True: if it is a valid placement
            False: if it is not a valid placement
        """

        pass

    def register_move(self, move) -> bool:
        """Registers a given move.

        Updates the board to include the most recent move.

        Args: 
            move: A list of tuples containing a tile and it's given indices 
                to represent the most recent move. For example:

                {(Tile 1, x cord 1, y cord 1), (Tile 2, x cord 2, y cord 2)...}
        
        Returns:
            Boolean corresponding to if the move was succesfully registered.
        """

    def score_move(self, move) -> int:
        """Scores a given move.

        Args:
            move: A list of placements containing a tile and it's given indices 
                to represent the most recent move. For example:

                {(Tile 1, x cord 1, y cord 1), (Tile 2, x cord 2, y cord 2)...}

        Returns: 
            Integer represent of the score of the move.
        """
