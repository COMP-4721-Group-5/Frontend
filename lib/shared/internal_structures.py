from typing import Dict, List, Final
from enum import IntEnum
import json

import numpy as np
import numpy.typing as npt


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

    Args:
        __color: color of the tile
        __shape: shape of the tile
        __temporary: boolean to tell if the tile is temporary
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

    def __json__(self) -> str:
        dict_form: Dict[str, bool | int] = {
            'tile_type': self.hex_value,
            'temporary': self.__temporary
        }
        return json.dumps(dict_form)

    @staticmethod
    def load_json(json_form: str):
        dict_form = json.loads(json_form)
        new_tile = Tile(0,0)
        new_tile.__color = dict_form['tile_type'] & 0x0f
        new_tile.__shape = dict_form['tile_type'] & 0xf0
        new_tile.__temporary = dict_form['temporary']
        return new_tile


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

    def __init__(self, tile: Tile, x_coord: int, y_coord: int):
        """Creates placement

        Args:
            tile: Tile of the specific placement
            x_coord: x coordinate of the placement
            y_coord: y coordinate of the placement
        """
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

    def __json__(self) -> str:
        dict_form: Dict[str, str | List[int]] = {
            'tile': self.__tile.__json__(),
            'pos': [self.x_coord, self.y_coord]
        }
        return json.dumps(dict_form)

    def load_json(json_form: str):
        dict_form = json.loads(json_form)
        new_placement = Placement(None,-1,-1)
        new_placement.tile = Tile.load_json(dict_form['tile'])
        new_placement.__x_coord = dict_form['pos'][0]
        new_placement.__x_coord = dict_form['pos'][1]
        return new_placement


class Board:
    """Contains the representation of the gameboard

    Attributes:
        board: a 217x217 array of Tiles
    """
    ROW: Final = 217
    COLUMN: Final = 217

    def __init__(self):
        """Inits the board"""
        self.__board = np.zeros((Board.ROW, Board.COLUMN), np.object_)

    def get_board(self) -> npt.NDArray[np.object_]:
        return self.__board

    def add_tile(self, placement: Placement):
        """Adds tile at given coordinates if there is no tile already there

        Args:
            placement: contains (Tile, x_coord, y_coord)
        """
        if self.__board[placement.x_coord, placement.y_coord] == 0:
            self.__board[placement.x_coord, placement.y_coord] = placement.tile

    def __json__(self) -> str:
        tile_pos = np.where(self.__board != 0)
        pos_tuples = list(zip(tile_pos[0], tile_pos[1]))
        dict_form = dict()
        for pos_tuple in pos_tuples:
            tile: Tile = self.__board[pos_tuple[0], pos_tuple[1]]
            dict_form[str(pos_tuple)] = tile.__json__()
        return json.dumps(dict_form)

    def load_json(self, json_form: str):
        dict_form: Dict[str, str] = json.loads(json_form)
        self.__board.fill(0)
        for pos_tuple in dict_form.keys():
            position = eval(pos_tuple)
            self.__board[position[0],position[1]] = Tile.load_json(dict_form[pos_tuple])


