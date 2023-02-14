import pytest

from lib.shared.internal_structures import *

@pytest.mark.parametrize("color", [
    TileColor.RED, TileColor.ORANGE, TileColor.YELLOW, TileColor.GREEN,
    TileColor.BLUE, TileColor.VIOLET
])
@pytest.mark.parametrize("shape", [
    TileShape.CIRCLE, TileShape.CLUB, TileShape.CROSS, TileShape.DIAMOND,
    TileShape.SQUARE, TileShape.STAR
])
def tile_json_test(color: TileColor, shape: TileShape):
    test_tile = Tile(color, shape)
    json_form = test_tile.__json__()
    assert test_tile == Tile.load_json(json_form)


@pytest.mark.parametrize("color", [
    TileColor.GREEN, TileColor.BLUE, TileColor.VIOLET
])
@pytest.mark.parametrize("shape", [
    TileShape.CIRCLE, TileShape.CLUB
])
@pytest.mark.parametrize("x", [
    124, 208, 34
])
@pytest.mark.parametrize("y", [
    146, 12, 32
])
def placement_json_test(color: TileColor, shape: TileShape, x: int, y: int):
    test_placement = Placement(Tile(color, shape), x, y)
    json_form = test_placement.__json__()
    assert test_placement == Placement.load_json(json_form)

def board_json_test():
    base_board = Board()
    base_board.get_board()[63,64] = Tile(TileColor.RED, TileShape.DIAMOND)
    copy_board = Board()
    copy_board.load_json(base_board.__json__())
    assert base_board.get_board()[63,64] == copy_board.get_board()[63,64]
