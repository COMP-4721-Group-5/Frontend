from internal_structures import *


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
            max line length is 5, does not include current placement
            returns None in both lists if there are no valid lines
        """
        x_line: list() = None
        y_line: list() = None
        y_count = 0
        x_count = 0
        skip = False
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
            if temp_tile.eq(placement.tile):
                y_line = None
                skip = True

        if skip is False: #If the y_line has a duplicate skip checking below as it is invalid placement
            for i in range(5): #Checks up to 5 tiles below the horizontal
                if placement.y_coord - i - 1 < 0:
                    break
                temp_tile = self.__board[placement.x_coord][placement.y_coord - i - 1]
                temp_placement = Placement(temp_tile, placement.x_coord, placement.y_coord - i - 1)
                if temp_tile is None:
                    break
                else:
                    if temp_tile.shape == placement.tile.shape or temp_tile.color == placement.tile.color:
                        y_line.append(temp_placement)
                        y_count += 1
                #Checks if line is too long or contains duplicate tiles
                if y_count > 5 or temp_tile.__eq__(placement.tile):
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
                if temp_tile.shape == placement.tile.shape or temp_tile.color == placement.tile.color:
                    x_line.append(temp_placement)
                    x_count += 1
                if temp_tile.__eq__(placement.tile): #if line already contains this tile, it is invalid
                    return None, y_line

        for i in range(5): #Checks up to 5 tiles to the left of the vertical
            if placement.x_coord + i + 1 > 217:
                break
            temp_tile = self.__board[placement.x_coord + i + 1][placement.y_coord]
            temp_placement = Placement(temp_tile, placement.x_coord, placement.y_coord)
            if temp_tile is None:
                break
            else:
                if temp_tile.shape == placement.tile.shape or temp_tile.color == placement.tile.color:
                    x_line.append(temp_placement)
                    x_count += 1
            #Checks if line is too large or if it already contains a given tile
            if x_count > 5 or temp_tile.__eq__(placement.tile):
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
        x_line, y_line = self.get_lines(placement)
        if x_line is None and y_line is None:
            return False
        else:

            return True

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

        Currently score relies on temporary tile information so scoring must happen before a move is fully
        registered
        Args:
            move: A list of placements containing a tile and it's given indices 
                to represent the most recent move. For example:

                {(Tile 1, x cord 1, y cord 1), (Tile 2, x cord 2, y cord 2)...}

        Returns: 
            Integer represent of the score of the move.
        """
        score = 0
        for placement in move:
            score += self.score_placement(placement)

        return score

    def score_placement(self, placement) -> int:
        """Scores a given placement

        Args: 
            placement: contains the placement data in the form of (Tile, x_coord, y_coord)

        Returns:
            Integer representation of the score of the move.
        """
        score = 0
        x_line, y_line = self.get_lines(placement)
        already_scored = False #Keeps track of whether the line(s) of placement have already been scored on this turn
        if x_line is not None:
            for placement in x_line:
                if placement.tile.is_temporary:
                    already_scored = True
            if already_scored:
                score += 1
            else:
                score += len(x_line) + 1
            if len(x_line) == 5: #Checks for Quirkle
                score += 6
        already_scored = False
        if y_line is not None:
            for placement in y_line:
                if placement.tile.is_temporary:
                    already_scored = True
            if already_scored:
                score += 1
            else:
                score += len(y_line)
            if len(y_line) == 5: #Checks for Quirkle
                score += 6
""" Testing
board = Board()

orange_square = Tile(TileColor.ORANGE, TileShape.SQUARE, False)
placement = Placement(orange_square, 0, 0)

board.add_tile(placement)

red_circle = Tile(TileColor.RED, TileShape.CIRCLE, True)
placement = Placement(red_circle, 0, 1)

rules = Gamerules()
b = board.get_board()
rules.update_board(b)
print(rules.verify_placement(placement))
print(rules.get_lines(placement))
"""