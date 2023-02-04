from lib.shared.internal_structures import Tile

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
