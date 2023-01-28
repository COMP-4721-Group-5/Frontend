class Logic:
    """ Controls all game logic.

    Responsible for recieving input messages from the player
    and verfiying the validity of the input. Passes the updated
    game state to the socket for transmission to the server
    Recieves game state data from the socket and updates the model
    accordingly. 

    Attributes:
        board: a 217x217 list of tiles that contains the state of the
            game board
        hand: a list of tiles of length 6 representing the hand of the player
        score: An integer count of the player's current score
    """
    hand = {}
    board ={}
    score = 0

    def verify_move(self, board, move):
        """Verifies the most recent move

        Ensures that a given move is legal by game rules.

        Args: 
            board: contains the current game board.
            move: A list of tuples containing a tile and it's given indices 
                to represent the most recent move. For example:

                {(Tile 1, x cord 1, y cord 1), (Tile 2, x cord 2, y cord 2)...}
        
        Returns: 
            Boolean corresponding to the validity of the move, true if the move is
                determined to be legal, false if it is not.
        """

    def register_move(self, board, move):
        """Registers a given move.

        Updates the board to include the most recent move.

        Args: 
            board: 217x217 list of tiles containing the current game board
            move: A list of tuples containing a tile and it's given indices 
                to represent the most recent move. For example:

                {(Tile 1, x cord 1, y cord 1), (Tile 2, x cord 2, y cord 2)...}
        
        Returns:
            Boolean corresponding to if the move was succesfully registered.
            
        """ 
    def score_move(self, move):
        """Scores a given move.

        Args:
            move: A list of tuples containing a tile and it's given indices 
                to represent the most recent move. For example:

                {(Tile 1, x cord 1, y cord 1), (Tile 2, x cord 2, y cord 2)...}

        Returns: 
            Integer represent of the score of the move.
        """
    
    def update_hand(self, hand):
        self.hand = hand
    
    def put_temp_move(self, move):
        """Receives a move from the view to be evaluated

        Args:
            move: A list of tuples containing a tile and it's given indices 
                to represent the most recent move. For example:

                {(Tile 1, x cord 1, y cord 1), (Tile 2, x cord 2, y cord 2)...}

        Returns:
            true: if the move is valid.
            false: if the move is invalid.
        """


        

