from typing import List

from .internal_structures import Placement, Board, Tile


class Gamerules:
    """A representation of the game's logic

    Responsible for ensuring consistency with game logic and contains methods for altering the board model
    as per legal moves by the game's rules.
    """

    def verify_move(self, move: List[Placement], board: Board):
        """Verifies the most recent move

        Ensures that a given move is legal by game rules.

        Args:
            move: A list of placements containing a tile and it's given indices
                to represent the most recent move. For example:

                {(Tile 1, x cord 1, y cord 1), (Tile 2, x cord 2, y cord 2)...}
            board: contains the game board

        Returns:
            A boolean list corresponding to the validity of the move, true if the move is
                determined to be legal, false if it is not.
        """
        for placement in move:
            if self.verify_placement(placement, board) is False:
                return False

        return True

    def get_lines(self, placement: Placement, board: Board):
        """Check which lines a given placement could be a part of

        Interated through the board from the placement data to see what valid lines configurations
        could be made.

        Args:
            placement: placement data of the tile
            board: 2d array containing all placement data

        Returns:
            A list of possible lines in form of a list of placements for ex:
                {Line:((Tile: red, circle, x, y), (Tile: red, square, x, y), (Tile: red, star, x, y)), Line:(Tile: green, square, Tile: red, square)}
            max line length is 5, does not include current placement
            returns None in a list that contains an invalid line
        """
        x_line = list()
        y_line = list()
        y_count = 0
        x_count = 0
        skip = False
        for i in range(5):  # Checks up to 5 tiles above the horizontal
            if placement.y_coord + i + 1 > 217:
                break
            temp_tile = board[placement.x_coord][placement.y_coord + i + 1]
            temp_placement = Placement(
                temp_tile, placement.x_coord, placement.y_coord + i + 1
            )
            if temp_tile is None:
                break
            else:
                if (
                    temp_tile.shape == placement.tile.shape
                    or temp_tile.color == placement.tile.color
                ):
                    y_line.append(temp_placement)
                    y_count += 1
                else:  # If the line contains an invalid match
                    y_line = None
                    break
            if temp_tile == placement.tile:
                y_line = None
                skip = True

        if (
            not skip
        ):  # If the y_line has a duplicate skip checking below as it is invalid placement
            for i in range(5):  # Checks up to 5 tiles below the horizontal
                if placement.y_coord - i - 1 < 0:
                    break
                temp_tile = board[placement.x_coord][placement.y_coord - i - 1]
                temp_placement = Placement(
                    temp_tile, placement.x_coord, placement.y_coord - i - 1
                )
                if temp_tile is None:
                    break
                else:
                    if (
                        temp_tile.shape == placement.tile.shape
                        or temp_tile.color == placement.tile.color
                    ):
                        y_line.append(temp_placement)
                        y_count += 1
                    else:  # If the line contains an invalid match
                        y_line = None
                        break
                # Checks if line is too long or contains duplicate tiles
                if y_count > 5 or temp_tile == placement.tile:
                    y_line = None
                    break

        # Gets the x_line
        for i in range(5):  # Checks up to 5 tiles to the right of the vertical
            if placement.x_coord - i - 1 < 0:
                break
            temp_tile = board[placement.x_coord - i - 1][placement.y_coord]
            temp_placement = Placement(
                temp_tile, placement.x_coord - i - 1, placement.y_coord
            )
            if temp_tile is None:
                break
            else:
                if (
                    temp_tile.shape == placement.tile.shape
                    or temp_tile.color == placement.tile.color
                ):
                    x_line.append(temp_placement)
                    x_count += 1
                else:  # if there is an invalid match in the line
                    x_line = None
                    break
            if temp_tile.__eq__(
                placement.tile
            ):  # if line already contains this tile, it is invalid
                return None, y_line

        for i in range(5):  # Checks up to 5 tiles to the left of the vertical
            if placement.x_coord + i + 1 > 217:
                break
            temp_tile = board[placement.x_coord + i + 1][placement.y_coord]
            temp_placement = Placement(
                temp_tile, placement.x_coord - i - 1, placement.y_coord
            )
            if temp_tile is None:
                break
            else:
                if (
                    temp_tile.shape == placement.tile.shape
                    or temp_tile.color == placement.tile.color
                ):
                    x_line.append(temp_placement)
                    x_count += 1
                else:
                    x_line = None
                    break
            # Checks if line is too large or if it already contains a given tile
            if x_count > 5 or temp_tile.__eq__(placement.tile):
                x_line = None
                break

        return x_line, y_line

    def verify_placement(self, placement: Placement, board: Board) -> bool:
        """Verifies placement of a single tile on the board

        Checks to make sure a given placement is a valid move.

        Args:
            placement: placement to verify
            board: board containing all current placements
        Return:
            True: if it is a valid placement
            False: if it is not a valid placement
        """
        x_line, y_line = self.get_lines(placement)
        if x_line == [] and y_line == [] or x_line is None or y_line is None:
            return False
        else:
            return True

    def register_move(self, move: List[Placement], board: Board) -> bool:
        """Registers a given move.

        Updates the board to include the most recent move.

        Args:
            move: A list of placements containing a tile and it's given indices
                to represent the most recent move. For example:

                {(Tile 1, x cord 1, y cord 1), (Tile 2, x cord 2, y cord 2)...}
            board: contains the game board as a 2d array

        Returns:
            Boolean corresponding to if the move was succesfully registered.
        """

    def score_move(self, move: List[Placement], board: Board) -> int:
        """Scores a given move.

        Currently score relies on temporary tile information so scoring must happen before a move is fully
        registered

        Args:
            move: A list of placements containing a tile and it's given indices
                to represent the most recent move. For example:

                {(Tile 1, x cord 1, y cord 1), (Tile 2, x cord 2, y cord 2)...}
            board: contains the game board

        Returns:
            Integer represent of the score of the move.
        """
        score = 0
        for placement in move:
            score += self.score_placement(placement, board)

        return score

    def score_placement(self, placement: Placement, board: Board) -> int:
        """Scores a given placement

        Args:
            placement: contains the placement data in the form of (Tile, x_coord, y_coord)
            board: contains the game board

        Returns:
            Integer representation of the score of the move.
        """
        score = 0
        x_line, y_line = self.get_lines(placement, board)
        already_scored = False  # Keeps track of whether the line(s) of placement have already been scored on this turn
        if x_line is not None:
            for placement in x_line:
                if placement.tile.is_temporary():
                    already_scored = True
            if already_scored == True:
                score += 1
            else:
                score += len(x_line) + 1
            if len(x_line) == 5:  # Checks for Quirkle
                score += 6
        already_scored = False
        if y_line is not None:
            for placement in y_line:
                if placement.tile.is_temporary():
                    already_scored = True
            if already_scored == True:
                score += 1
            else:
                score += len(y_line) + 1
            if len(y_line) == 5:  # Checks for Quirkle
                score += 6
        return score

    def remove_placement(self, placement: Placement, board: Board):
        """Removes a given placement

        Args:
            placement: the placement to be removed
            board: contains the current game board

        Returns:
            An integer representing the amount of points need to be deducted from the player's score. Returns -1 for invalid and unsuccessful removal
        """
        if not placement.tile.is_temporary():
            return -1

        x_line, y_line = self.get_lines(placement, board)

        x_length = x_line.__len__() + 1
        y_length = y_line.__len__() + 1
        scoreRemoval = 0

        if x_length == 6:  # Removes Quirkle points
            scoreRemoval += 6

        hasTemp = False
        for placement in x_line:
            if placement.tile.is_temporary():
                hasTemp = True
        if hasTemp:
            scoreRemoval += 1
        else:
            scoreRemoval += x_length
            print(x_length)

        if y_length == 6:  # Removes Quirkle points
            scoreRemoval += 6

        hasTemp = False
        for placement in y_line:
            if placement.tile.is_temporary():
                hasTemp = True
        if hasTemp:
            scoreRemoval += 1
        else:
            scoreRemoval += y_length
            print(y_length)

        return scoreRemoval
