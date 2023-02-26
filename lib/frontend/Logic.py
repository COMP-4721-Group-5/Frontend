from typing import List

from ..shared.internal_structures import Board, Placement, Tile, TileColor, TileShape
from ..shared.player import Player
from ..shared import gamerules


class Logic:
    """ Controls all game logic.

    Responsible for recieving input messages from the player
    and verfiying the validity of the input. Passes the updated
    game state to the socket for transmission to the server
    Recieves game state data from the socket and updates the model
    accordingly. 

    Attributes:
        board: Contains the board
        tempMove: List that contains all temporary placements of current players move
        player: Contains the local player's data 
        bag: contains the bag of tiles left to be drawn
        is_first_turn: a boolean variable to keep track of whether or not it is the first move
        is_curr_turn: a boolean variable to keep track of if it is this player's turn
    """
    __board: Board
    __tempMove: Placement
    __player: Player
    __bag: List[Tile]
    __is_first_turn: bool
    __is_curr_turn: bool

    def __init__(self) -> None:
        """Inits the game with one player"""
        self.is_curr_turn = False
        self.is_first_turn = False
        self.start_game(1)

    def start_game(self, playerCount: int):
        """Collects playerCount data and sends a message to the socket to start the game

        !!!Right now acting as a temporary method for demo purposes
        Args:
            playerCount: amount of players in the game
        """
        self.__board = Board()
        self.__player = Player()
        self.__bag = list()

        for color in TileColor:
            for shape in TileShape:
                tile = Tile(color, shape, True)
                self.__bag.append(tile)

        temp_hand = []
        for i in range(6):
            temp_hand.append(self.__bag.pop())

        self.__player.update_hand(temp_hand)

    def play_tile(self, placement, index):
        """Plays a tile given an index and desired placement

        Args:
            placement: desired placement of the tile, contains tile, x_coord and y_coord data
            index: index of the tile within the players hand
        """
        self.board.add_tile(placement)
        self.player.play_tile(index)

    @property
    def board(self):
        return self.__board

    @board.setter
    def board(self, board: Board):
        """Updates the board

        Args:
            board: new board
        """
        if not isinstance(board, Board):
            raise TypeError
        self.__board = board

    @property
    def player(self):
        return self.__player
    

    @player.setter
    def player(self, new_player: Player):
        if not isinstance(new_player, Player):
            raise TypeError
        self.__player = new_player

    @property
    def is_first_turn(self):
        return self.__is_first_turn
    
    @is_first_turn.setter
    def is_first_turn(self, is_first_turn: bool):
        if not isinstance(is_first_turn, bool):
            raise TypeError
        self.is_first_turn = is_first_turn
    
    @property
    def is_curr_turn(self):
        return self.__is_curr_turn
    
    @is_first_turn.setter
    def is_curr_turn(self, is_curr_turn: bool):
        if not isinstance(is_curr_turn, bool):
            raise TypeError
        self.is_curr_turn = is_curr_turn
    