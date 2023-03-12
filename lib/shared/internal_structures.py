from abc import ABC, abstractmethod
from typing import Any, Dict, List, Final
from enum import IntEnum
import json

import numpy as np
import numpy.typing as npt


class JsonableObject(ABC):
    """Base class of objects that can be represented as JSON.
    
    Subclasses of this object support conversion to / from
    its JSON form.
    """

    @abstractmethod
    def json_serialize(self) -> Dict[str, Any]:
        """Returns JSON representation of this object.

        Returns:
            JSON-serializable form of this object
        """
        pass

    @staticmethod
    @abstractmethod
    def json_deserialize(serialized_form: Dict[str, Any]):
        """Constructs object of this type from JSON serialized form
        
        Args:
            json_form: JSON serialized form of an object of this type
        
        Returns:
            Object of this type that the argument represents
        """
        pass


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


class Tile(JsonableObject):
    """
    Python representation of a Quirkle tile

    Args:
        __color: color of the tile
        __shape: shape of the tile
        __temporary: boolean to tell if the tile is temporary
    """
    JSONABLE_TYPE: Final[str] = 'tile'
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

    def __repr__(self) -> str:
        if self.__temporary:
            return 'Temporary %s %s tile' % (self.__color.name,
                                             self.__shape.name)
        else:
            return '%s %s tile' % (self.__color.name, self.__shape.name)

    def json_serialize(self) -> Dict[str, bool | int]:
        dict_form: Dict[str, bool | int] = {
            'type': Tile.JSONABLE_TYPE,
            'tile_type': self.hex_value,
            'temporary': self.__temporary
        }
        return dict_form

    @staticmethod
    def json_deserialize(serialized_form: Dict[str, bool | int]):
        if type(serialized_form) is not dict:
            raise TypeError
        new_tile = Tile(0, 0)
        new_tile.__color = TileColor(serialized_form['tile_type'] & 0x0f)
        new_tile.__shape = TileShape(serialized_form['tile_type'] & 0xf0)
        new_tile.__temporary = serialized_form['temporary']
        return new_tile


class Placement(JsonableObject):
    """Contains placement data

    Attributes:
        tile: tile to be placed
        x_coord: x coordinate of the tile to be placed within the game board
        y_coord: y coordinate of the tile to be placed within the game board
    """
    JSONABLE_TYPE: Final[str] = 'placement'
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

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, Placement):
            return self.__tile == __o.__tile and self.__x_coord == __o.__x_coord and self.__y_coord == __o.__y_coord
        else:
            return False

    def __repr__(self) -> str:
        return '%s at (%d, %d)' % (self.__tile.__repr__(), self.x_coord,
                                   self.y_coord)

    def json_serialize(self) -> Dict[str, str | Tile | List[int]]:
        dict_form: Dict[str, str | Tile | List[int]] = {
            'type': Placement.JSONABLE_TYPE,
            'tile': self.__tile.json_serialize(),
            'pos': [self.x_coord, self.y_coord]
        }
        return dict_form

    @staticmethod
    def json_deserialize(serialized_form: Dict[str, str | Tile | List[int]]):
        if type(serialized_form) is not dict:
            raise TypeError
        new_placement = Placement(None, -1, -1)
        new_placement.__tile = serialized_form['tile']
        new_placement.__x_coord = serialized_form['pos'][0]
        new_placement.__y_coord = serialized_form['pos'][1]
        return new_placement


class Board(JsonableObject):
    """Contains the representation of the gameboard

    Attributes:
        board: a 217x217 array of Tiles
    """
    JSONABLE_TYPE: Final[str] = 'board'
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

    def remove_tile(self, x, y):
        """Removes a tile at a given x and y
        
        Args:
            x: x coordinate
            y: y coordinate
        Returns: the tile that was removed
        """
        tile = self.__board[x][y]
        self.__board[x][y] = 0
        return tile

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, Board):
            self_tile_pos = np.where(self.__board != 0)
            self_pos_tuples = list(zip(self_tile_pos[0], self_tile_pos[1]))
            other_tile_pos = np.where(__o.__board != 0)
            other_pos_tuples = list(zip(other_tile_pos[0], other_tile_pos[1]))
            if len(self_pos_tuples) != len(other_pos_tuples):
                return False
            for self_pos_tuple in self_pos_tuples:
                if self_pos_tuple not in other_pos_tuples:
                    return False
                elif self.__board[self_pos_tuple[0],
                                  self_pos_tuple[1]] != __o.__board[
                                      self_pos_tuple[0], self_pos_tuple[1]]:
                    return False
            return True
        else:
            return False

    def json_serialize(self) -> Dict[str, Dict[str, bool | int]]:
        tile_pos = np.where(self.__board != 0)
        pos_tuples = list(zip(tile_pos[0], tile_pos[1]))
        dict_form = dict()
        dict_form['type'] = Board.JSONABLE_TYPE
        for pos_tuple in pos_tuples:
            tile: Tile = self.__board[pos_tuple[0], pos_tuple[1]]
            dict_form[str(pos_tuple)] = tile.json_serialize()
        return dict_form

    def json_deserialize(serialized_form: Dict[str, Dict[str, bool | int]]):
        if type(serialized_form) is not dict:
            raise TypeError
        new_board = Board()
        for pos_tuple in serialized_form.keys():
            if pos_tuple != 'type':
                position = eval(pos_tuple)
                new_board.__board[position[0],
                                  position[1]] = serialized_form[pos_tuple]
        return new_board
