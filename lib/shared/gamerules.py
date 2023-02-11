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
            A list of possible lines in form of a list of placements for ex:
                {Line:((Tile: red, circle, x, y), (Tile: red, square, x, y), (Tile: red, star, x, y)), Line:(Tile: green, square, Tile: red, square)}
            max line length is 6
        """
        x_line = list()
        y_line = list()
        #y_line = self.__board[placement.x_coord][placement.y_coord - 6:placement.y_coord + 6]
        #x_line = self.__board[placement.x_coord - 6:placement.x_coord + 6][placement.y_coord]
        y_count = 0
        x_count = 0
        for i in range(5): #Checks up to 5 tiles above the horizontal
            if placement.y_coord + i + 1 > 217:
                break
            temp_tile = self.__board[placement.x_coord][placement.y_coord + i + 1]
            temp_placement = Placement(temp_tile, placement.x_coord, placement.y_coord + i + 1)
            if temp_tile is None:
                break
            else:
                if temp_tile.shape() == placement.tile.shape() or temp_tile.color() == placement.tile.color():
                    y_line.append(temp_placement)
                    y_count += 1

        for i in range(5): #Checks up to 5 tiles below the horizontal
            if placement.y_coord - i - 1 < 0:
                break
            temp_tile = self.__board[placement.x_coord][placement.y_coord - i - 1]
            temp_placement = Placement(temp_tile, placement.x_coord, placement.y_coord - i - 1)
            if temp_tile is None:
                break
            else:
                if temp_tile.shape() == placement.tile.shape() or temp_tile.color() == placement.tile.color():
                    y_line.append(temp_placement)
                    y_count += 1
            if y_count > 6:
                y_line = None
                break

        #Gets the x_line
        for i in range(5): #Checks up to 5 tiles to the right of the vertical
            if placement.x_coord - i - 1 < 0:
                break
            temp_tile = self.__board[placement.x_coord - i - 1][placement.y_coord]
            temp_placement = Placement(temp_tile, placement.x_coord, placement.y_coord)
            if temp_tile is None:
                break
            else:
                if temp_tile.shape() == placement.tile.shape() or temp_tile.color() == placement.tile.color():
                    x_line.append(temp_placement)
                    x_count += 1

        for i in range(5): #Checks up to 5 tiles to the left of the vertical
            if placement.x_coord + i + 1 > 217:
                break
            temp_tile = self.__board[placement.x_coord + i + 1][placement.y_coord]
            temp_placement = Placement(temp_tile, placement.x_coord, placement.y_coord)
            if temp_tile is None:
                break
            else:
                if temp_tile.shape() == placement.tile.shape() or temp_tile.color() == placement.tile.color():
                    x_line.append(temp_placement)
                    x_count += 1
            if x_count > 6:
                x_line = None
                break

            
        return x_line, y_line

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
