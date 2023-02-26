import pytest

from lib.shared.internal_structures import *
from lib.shared.network_exchange_format import JsonableEncoder
from lib.shared.network_exchange_format import JsonableDecoder


@pytest.mark.parametrize("color", [
    TileColor.RED, TileColor.ORANGE, TileColor.YELLOW, TileColor.GREEN,
    TileColor.BLUE, TileColor.VIOLET
])
@pytest.mark.parametrize("shape", [
    TileShape.CIRCLE, TileShape.CLUB, TileShape.CROSS, TileShape.DIAMOND,
    TileShape.SQUARE, TileShape.STAR
])
def test_tile_json(color: TileColor, shape: TileShape):
    test_tile = Tile(color, shape)
    assert test_tile == json.loads(json.dumps(test_tile, cls=JsonableEncoder),
                                   cls=JsonableDecoder)


@pytest.mark.parametrize("color",
                         [TileColor.GREEN, TileColor.BLUE, TileColor.VIOLET])
@pytest.mark.parametrize("shape", [TileShape.CIRCLE, TileShape.CLUB])
@pytest.mark.parametrize("x", [124, 208, 34])
@pytest.mark.parametrize("y", [146, 12, 32])
def test_placement_json(color: TileColor, shape: TileShape, x: int, y: int):
    test_placement = Placement(Tile(color, shape), x, y)
    assert test_placement == json.loads(json.dumps(test_placement,
                                                   cls=JsonableEncoder),
                                        cls=JsonableDecoder)


def test_board_json():
    base_board = Board()
    base_board.get_board()[63, 64] = Tile(TileColor.RED, TileShape.DIAMOND)
    assert base_board == json.loads(json.dumps(base_board, cls=JsonableEncoder),
                                    cls=JsonableDecoder)
