import pytest

from lib.shared.internal_structures import *


@pytest.mark.parametrize(
    "color",
    [
        TileColor.RED,
        TileColor.ORANGE,
        TileColor.YELLOW,
        TileColor.GREEN,
        TileColor.BLUE,
        TileColor.VIOLET,
    ],
)
@pytest.mark.parametrize(
    "shape",
    [
        TileShape.CIRCLE,
        TileShape.CLUB,
        TileShape.CROSS,
        TileShape.DIAMOND,
        TileShape.SQUARE,
        TileShape.STAR,
    ],
)
def test_tile_hex(color: TileColor, shape: TileShape):
    test_tile = Tile(color, shape)
    assert test_tile.color == color
    assert test_tile.shape == shape
    assert test_tile.hex_value == color.value ^ shape.value
