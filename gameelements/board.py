class Board:
    """Contains the representation of the gameboard

    Attributes:
        board: a 217x217 array of Tiles
    """
    board = {}
    rows, cols = (217, 217)

    def __init__(self):
        board = [[None]*self.cols]*self.rows

    def get_board(self):
        return self.board
    
   
    def add_tile(self, placement):
        """Adds tile at given coordinates

        Args:
        placement: contains (Tile, x_coord, y_coord)
        """
        self.board[placement.x_coord][placement.y_coord] = placement.tile

    