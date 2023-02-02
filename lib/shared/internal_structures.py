from enum import Enum


class TileColor(Enum):
    """
    Set of constants defining color of a tile
    """
    RED = 0x01
    ORANGE = 0x02
    YELLOW = 0x03
    GREEN = 0x04
    BLUE = 0x05
    VIOLET = 0x06


class TileShape(Enum):
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
        Hexadecimal value uniquely representing type of this tyle
        """
        return self.color.value ^ self.shape.value

    def is_temporary(self):
        """
        Checks whether this tile is marked as temporary
        """
        return self.__temporary

    def set_permanent(self):
        """
        Marks this tile as permanent
        """
        self._temporary = False

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, Tile):
            return self.__color == __o.__color and self.__shape == __o.__shape and self.__temporary == __o.__temporary
        else:
            return False
