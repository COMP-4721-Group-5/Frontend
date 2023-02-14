from typing import List

from ..shared.internal_structures import Board, Placement, Tile, TileColor, TileShape
from ..shared.player import Player
from ..shared import gamerules

import random

class Logic_backend:
    """Server that manages all players (Clients) data (receiving, checking and updating).
    
    Responsible for keeping track of all player's data,
    initialize players's hand, receive and verify player's move, checking for winner
    and update last player's move to other player's board as well as announce the winner (if happen),
    restock player's hand, calculate player's score after their valid move.
    
    Attributes:
        gameRules: has useful functions to help verify valid move and winner.
        board: Contains the board
        tempMove: List that contains all temporary placements of current players move
        player: Contains the local player's data 
        bag: list of all tiles in game
        playerCount: number of players/number of clients connect to the server
    """
    
    __gameRules: gamerules
    __board: Board
    __tempMove: Placement
    __player: Player 
    __bag: List[Tile]
    __playerCount: int 
    #__playerList: List[Player] -> list of players to keep track of score and update move

    def __init__(self) -> None:
        """Inits the game with the amount of joining players"""

        self.__board = Board()      
        #self.__player = Player() -> may not needed
        self.__bag = list()
        #self.__playerList = list()
        #self.__gameRules = Gamerules()
        #self.__playerCount = 0

        self.start_game(self.__playerCount)
        
    def set_playerCount(self, num: int):
        """To assign the number of players (clients) to class attribute (__playerCount)
        
        Args:
            num: number of players
        """
        self.__playerCount = num
    
    def start_game(self, playerCount: int):
        """should this appear?
        """
        self.__board.get_board()
        self.init_draw(playerCount)
        
        #while !self.check_for_winner:
        
        
    def init_draw(self, playerCount: int):
        """Initialize each player's hand
        
        Args:
            playerCount: number of players
        
        Returns: a 2D array which contains each player (represented by index) list
        of first drawn tiles 
        """
        init_tile_list = [playerCount][6]
        
        for color in TileColor:
            for shape in TileShape:
                tile = Tile(color, shape, True)
                self.__bag.append(tile)
                
        for i in range (playerCount):
            for j in range(6):
                init_tile_list[i][j] = random.choice(self.__bag.pop())
                  
        return init_tile_list
         
    def restock_tile(self, player_hand: List[Tile]):
        """Count the current number of tiles on player's hand then
        restock if needed (when < 6)
        
        Args: 
            player_hand: player's list of tiles
        
        Returns: list of tiles with possibly newly added tiles
        """
        if len(player_hand) < 6:
            while len(player_hand) < 6:
                player_hand.append(self.__bag.pop())
        return player_hand
    
    
    def received_move():  
        """Receive move from player, assign to __tempMove.
        
        Returns: void
        """
        pass
        
    def verify_move(move) -> bool:
        """Verify whether player's move is valid, call Gamerules to support
        
        Args: 
            move: player's move
        
        Returns: True if valid, else is False
        """ 
        pass
        
    def update_score():
        """ Update score to that one player having move to be verified
        Call Gamerules to calculate score
        
        Args:
            player: the player that has move be verified ??? 

        Returns:  void
        """
        pass
        
    def update_board(self):
        """Update last player's move (if valid) to other players's board view
        IF there is a winner, announce to every player and stop the game"""
        
        if self.check_for_winner() == True:
            self.announce_winner()
        pass
            
    def check_for_winner(self) -> bool:
        """Call Gamerules to check for winner
        Meanwhile keep track of every player's score 
        
        Returns: True if last player win, False if else
        """
        #player's instance 'score' and getter/sett funct
        
    def announce_winner():
        """Send message to player that the winner is found, and they lose."""


    def addPlayer(self, player: Player):
        """Create (add) a list of player from client data received by Socket, to keep track of them"""
        self.__playerCount = self.__playerCount + 1
    
    @property       #unsure
    def board(self):
        return self.__board    
    
    @property       #unsure
    def playerCount(self):
        return self.__playerCount
    
    @property
    def player(self):
        return self.__player