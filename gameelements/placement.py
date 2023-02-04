class Placement:
    """Contains placement data

    Attributes:
        tile: tile to be placed
        x_coord: x coordinate of the tile to be placed within the game board
        y_coord: y coordinate of the tile to be placed within the game board
    """
    tile = None
    x_coord = 0
    y_coord = 0

    """Creates placement
    """
    def __init__(self, tile, x_coord, y_coord):
        self.tile = tile
        self.x_coord = x_coord
        self.y_coord = y_coord