from typing import Final, List

from placement import Placement
from lib.shared.internal_structures import Tile

class Board:
    """Contains the representation of the gameboard

    Attributes:
        board: a 217x217 array of Tiles
    """
    __board: List[List[Tile]]
    ROW: Final = 217
    COLUMN: Final = 217

    def __init__(self):
        self.__board = [[None] * Board.COLUMN] * Board.ROW

    def get_board(self) -> List[List[Tile]]:
        return self.__board
    
   
    def add_tile(self, placement: Placement):
        """Adds tile at given coordinates

        Args:
        placement: contains (Tile, x_coord, y_coord)
        """
        self.board[placement.x_coord][placement.y_coord] = placement.tile

    