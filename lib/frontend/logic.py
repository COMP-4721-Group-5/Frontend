from typing import List

from ..shared.internal_structures import Board, Placement, Tile, TileColor, TileShape
from ..shared.player import Player
from ..shared import gamerules
from .frontend_network import ClientSocket, ClientRequest


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
        discards: keeps track of tiles to discard
    """
    __board: Board
    __temp_move: List[Placement]
    __player: Player
    __bag: List[Tile]
    __is_first_turn: bool
    __is_curr_turn: bool
    __discards: List[Tile]

    def __init__(self) -> None:
        """Inits the game with one player"""
        self.__temp_move = list()
        self.__discards = list()
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

    def play_tile(self, placement: Placement):
        """Plays a tile given an index and desired placement

        Args:
            placement: desired placement of the tile, contains tile, x_coord and y_coord data
        """
        self.__temp_move.append(placement)

    def undo_play(self, placement: Placement):
        """Undoes a given placement
        
        Removes tile from the temp_move list and places it back into the player's hand
        Args: 
            Tile: tile to place back in the hand
        """
        self.__temp_move.remove(placement)

    def discard_tile(self, tile: Tile, index: int):
        """Discards a tile at a given index

        Removes tiles from player's hand and places into the discard list
        Args:
            tile: tile to discard
            index: index of tile within the hand
        """
        self.player.play_tile(index)
        self.__discards.insert(index, tile)

    def undo_discard(self, index):
        """Undoes a given discard

        Removes the discarded tile from discar list and places it back into the players hand
        Args:
            index: index of tile in question in the player's hand
        """
        tile = self.__discards.pop(index)
        t_hand = self.player.get_hand()
        t_hand.append(tile)
        self.player.update_hand(t_hand)

    def end_turn(self, discard: bool, client_socket: ClientSocket):
        """Ends the current turn

        Args:
            discard: keeps track of whether or not the player chose to discard this turn
        """
        self.__is_curr_turn = False

        if discard:
            request = ClientRequest('discard', self.__discards)
            client_socket.send_data(request)
        else:
            request = ClientRequest('placement', self.__temp_move)
            client_socket.send_data(request)

        self.__discards = list()
        self.__temp_move = list()

    def tile_played(self):
        """Checks if a tile has been played
        Returns:
            True: if true
            False: if false
        """
        if len(self.__temp_move) == 0:
            return True
        return False

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
        self.__is_first_turn = is_first_turn

    @property
    def is_curr_turn(self):
        return self.__is_curr_turn

    @is_curr_turn.setter
    def is_curr_turn(self, is_curr_turn: bool):
        if not isinstance(is_curr_turn, bool):
            raise TypeError
        self.__is_curr_turn = is_curr_turn
