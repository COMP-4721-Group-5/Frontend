import unittest

from lib.shared.internal_structures import *

class TileTest(unittest.TestCase):

    def test_tile_hex(self):
        red_circle = Tile(TileColor.RED, TileShape.CIRCLE)
        self.assertEqual(red_circle.hex_value, 0x11)
