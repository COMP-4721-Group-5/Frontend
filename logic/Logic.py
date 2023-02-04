from gamerules import Gamerules
from lib import internal_structures
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
    board = {}
    tempMove = {}
    player = None
    bag = {}


    def start_game(self, playerCount):
        """Collects playerCount data and sends a message to the socket to start the game

        !!!Right now acting as a temporary method for demo purposes
        Args:
            playerCount: amount of players in the game
        """
        board = Board()
        Joe = Player()
        Joe.update_hand({})


        pass
    
    start_game(1)

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
    

    def place_temp_tile(self, placement):
        """Places a temporary tile on the board

        Places temporary tile on the board and checks validity of placement
        to render the action on the view

        Args:
            placement: Placement object containing the placement data
        """
        valid = gamerules.verify_placement(placement)
        if valid:
            tempMove.add(placement)
            return True
        else:
            return False

    def remove_tiles(self, indices):
        """Removes certain tiles from a player's hand at the given indices
    
        Args:
            indices: indices of the tiles that must be removed from player's hand
        """
        pass

    def update_hand(self, hand):
        """Updates the hand when refilled from bag
        
        Gets updated hand information from socket and updates the hand accordingly
        """
        self.hand = hand

    def update_view(self):
        """Updates the view

        Will be called after every placement check to update the view with validity information
        """
        pass

    def update_board(self, board):
        self.board = board

    