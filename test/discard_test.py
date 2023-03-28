from typing import List

import pytest

from lib.backend.Logic_backend import QwirkeleController
from lib.shared.internal_structures import Tile, TileColor, TileShape
from lib.shared.player import Player


@pytest.mark.parametrize(
    "discard, exp",
    [
        ([Tile(TileColor.RED, TileShape.CIRCLE)], True),
        (
            [
                Tile(TileColor.RED, TileShape.CIRCLE),
                Tile(TileColor.GREEN, TileShape.DIAMOND),
            ],
            True,
        ),
        (
            [
                Tile(TileColor.RED, TileShape.CIRCLE),
                Tile(TileColor.GREEN, TileShape.SQUARE),
            ],
            False,
        ),
        (
            [
                Tile(TileColor.RED, TileShape.CIRCLE),
                Tile(TileColor.RED, TileShape.CIRCLE),
            ],
            False,
        ),
    ],
)
def test_valid_discard(discard: List[Tile], exp: bool):
    test_player = Player()
    test_player[0] = Tile(TileColor.RED, TileShape.CIRCLE)
    test_player[1] = Tile(TileColor.GREEN, TileShape.DIAMOND)
    test_player[2] = Tile(TileColor.YELLOW, TileShape.SQUARE)
    test_player[3] = Tile(TileColor.VIOLET, TileShape.CIRCLE)
    test_player[4] = Tile(TileColor.BLUE, TileShape.STAR)
    test_player[5] = Tile(TileColor.RED, TileShape.CROSS)
    assert exp == QwirkeleController.is_valid_discard(test_player, discard)
