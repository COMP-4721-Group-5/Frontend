from typing import List, Final
from enum import IntEnum


class TileColor(IntEnum):
    """
    Set of constants defining color of a tile
    """
    RED = 0x01
    ORANGE = 0x02
    YELLOW = 0x03
    GREEN = 0x04
    BLUE = 0x05
    VIOLET = 0x06


class TileShape(IntEnum):
    """
    Set of constants defining shape of a tile
    """
    CIRCLE = 0x10
    CROSS = 0x20
    DIAMOND = 0x30
    SQUARE = 0x40
    STAR = 0x50
    CLUB = 0x60


class Tile:
    """
    Python representation of a Quirkle tile
    """
    __color: TileColor
    __shape: TileShape
    __temporary: bool

    def __init__(self,
                 color: TileColor,
                 shape: TileShape,
                 temp: bool = True) -> None:
        self.__color = color
        self.__shape = shape
        self.__temporary = temp

    @property
    def color(self):
        """
        Color of this tile
        """
        return self.__color

    @property
    def shape(self):
        """
        Shape of this tile
        """
        return self.__shape

    @property
    def hex_value(self):
        """
        Hexadecimal value uniquely representing type of this tile

        Returns: 
            Specific hex value for the tile type
        """
        return self.color.value ^ self.shape.value

    def is_temporary(self):
        """
        Checks whether this tile is marked as temporary

        Returns:
            boolean value of whether or not the tile is temporary
        """
        return self.__temporary

    def set_permanent(self):
        """
        Marks this tile as permanent
        """
        self._temporary = False

    def __eq__(self, __o: object) -> bool:
        """Checks if two tiles are equal

        Returns:
            True: if they are
            False: if not
        """
        if isinstance(__o, Tile):
            return self.__color == __o.__color and self.__shape == __o.__shape and self.__temporary == __o.__temporary
        else:
            return False

class Placement:
    """Contains placement data

    Attributes:
        tile: tile to be placed
        x_coord: x coordinate of the tile to be placed within the game board
        y_coord: y coordinate of the tile to be placed within the game board
    """
    __tile: Tile
    __x_coord: int
    __y_coord: int

    """Creates placement
    """
    def __init__(self, tile: Tile, x_coord: int, y_coord: int):
        self.__tile = tile
        self.__x_coord = x_coord
        self.__y_coord = y_coord

    @property
    def tile(self):
        return self.__tile
    
    @property
    def x_coord(self):
        return self.__x_coord

    @property
    def y_coord(self):
        return self.__y_coord

class Board:
    """Contains the representation of the gameboard

    Attributes:
        board: a 217x217 array of Tiles
    """
    __board: List[List[Tile]]
    ROW: Final = 217
    COLUMN: Final = 217

    def __init__(self):
        self.__board = list()
        for i in range(Board.COLUMN):
            self.__board.append([None] * Board.COLUMN)

    def get_board(self) -> List[List[Tile]]:
        return self.__board
    
   
    def add_tile(self, placement: Placement):
        """Adds tile at given coordinates

        Args:
        placement: contains (Tile, x_coord, y_coord)
        """
        if self.__board[placement.x_coord][placement.y_coord] == None:
            self.__board[placement.x_coord][placement.y_coord] = placement.tile
