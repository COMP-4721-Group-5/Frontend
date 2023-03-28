from typing import List

import pytest

from lib.shared.gamerules import Gamerules
from lib.shared.internal_structures import Board, Placement, Tile, TileColor, TileShape


@pytest.mark.parametrize(
    "board, placements, result",
    [
        (Board(), [Placement(Tile(TileColor.BLUE, TileShape.DIAMOND), 110, 110)], True),
        (
            Board(),
            [
                Placement(Tile(TileColor.BLUE, TileShape.DIAMOND), 110, 110),
                Placement(Tile(TileColor.BLUE, TileShape.SQUARE), 110, 111),
            ],
            True,
        ),
        (
            Board(),
            [
                Placement(Tile(TileColor.BLUE, TileShape.DIAMOND), 110, 110),
                Placement(Tile(TileColor.RED, TileShape.SQUARE), 110, 111),
            ],
            False,
        ),
    ],
)
def test_move(board: Board, placements: List[Placement], result: bool):
    rule = Gamerules()
    assert result == rule.verify_move(placements, board)
