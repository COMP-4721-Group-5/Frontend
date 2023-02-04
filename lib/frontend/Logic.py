from ..shared.internal_structures import Board, Placement, Tile
from ..shared.player import Player
from ..shared import gamerules
from typing import List
class Logic:
    """ Controls all game logic.

    Responsible for recieving input messages from the player
    and verfiying the validity of the input. Passes the updated
    game state to the socket for transmission to the server
    Recieves game state data from the socket and updates the model
    accordingly. 

    Attributes:
        board: Contains the board
        tempMove: Contains all temporary placements of current players move
        player: Contains the local player's data 
    """
    board: Board
    tempMove: Placement
    player: Player
    bag: List[Tile]

    def __init__(self) -> None:
        self.start_game()

    def start_game(self):
        """Collects playerCount data and sends a message to the socket to start the game

        !!!Right now acting as a temporary method for demo purposes
        Args:
            playerCount: amount of players in the game
        """
        board = Board()
        player = Player()

        for color in Tile.color:
            for shape in Tile.shape:
                tile = Tile(color, shape, True)
                self.bag.append(Tile)

        temp_hand = {}
        for i in range(6):
            temp_hand.add(self.bag.pop())
        
        player.update_hand(temp_hand)

    def put_temp_move(self, move):
        """Receives a move from the view to be evaluated

        Args:
            move: A list of placements containing a tile and it's given indices 
                to represent the most recent move. For example:

                {(Tile 1, x cord 1, y cord 1), (Tile 2, x cord 2, y cord 2)...}

        Returns:
            true: if the move is valid.
            false: if the move is invalid.
        """
        gamerules.verify_move(move)
        pass
    

    def place_temp_tile(self, placement: Placement):
        """Places a temporary tile on the board

        Places temporary tile on the board and checks validity of placement
        to render the action on the view

        Args:
            placement: Placement object containing the placement data
        """
        self.board.add_tile(placement)

        """
        valid = gamerules.verify_placement(placement)
        if valid:
            gamerules.tempMove.add(placement)
            return True
        else:
            return False
        """

    def update_board(self, board: Board):
        self.board = board

    