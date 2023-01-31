import gamerules
class Logic:
    """ Controls all game logic.

    Responsible for recieving input messages from the player
    and verfiying the validity of the input. Passes the updated
    game state to the socket for transmission to the server
    Recieves game state data from the socket and updates the model
    accordingly. 

    Attributes:
        board: Contains the board
    """
    board = {}
    rules = gamerules()

    """Collects playerCount data and sends a message to the socket to start the game

    Args:
        playerCount: amount of players in the game
    """
    def start_game(self, playerCount):
        pass
    
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

    def update_board(self, board):
        self.board = board