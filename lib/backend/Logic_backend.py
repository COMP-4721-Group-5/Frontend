from queue import Queue
import random as rand
from typing import List

from .server_components import ClientConnection
from .server_components import Request
from ..shared.internal_structures import Board
from ..shared.internal_structures import Tile
from ..shared.internal_structures import TileColor
from ..shared.internal_structures import TileShape
from ..shared.network_exchange_format import ServerResponse
from ..shared.gamerules import Gamerules

class QwirkeleController:
    """Root controller for Qwirkle Server

    Attributes:
        clients: Clients connected to this server
        requests: Queue of requests from clients
        board: Internal board instance
        tile_bag: Bag of tiles
        active: Indicates current state of server
        curr_player: Current player in turn
        gamerules: set of gamerules
    """
    __clients: List[ClientConnection]
    __requests: Queue[Request]
    __board: Board
    __tile_bag: List[Tile]
    __active: bool
    __curr_player: int
    __gamerules: Gamerules

    def __init__(self, client_list: List[ClientConnection],
                 request_queue: Queue[Request]) -> None:
        self.__clients = client_list
        self.__requests = request_queue
        self.__curr_player = 0
        self.__active = True
        self.__board = Board()
        self.__tile_bag = list()
        self.__gamerules = Gamerules()
        for i in range(3):
            for color in TileColor:
                for shape in TileShape:
                    self.__tile_bag.append(Tile(color, shape))
        for client in self.__clients:
            for i in range(6):
                # Add tiles to player
                client.get_player()[i] = self.__tile_bag.pop(
                    rand.randrange(len(self.__tile_bag)))
        self.sync_all_players()

    def process_request(self):
        """Processes a request from client
        """
        curr_request = self.__requests.get()
        # use curr_request.data to access the content of request directly
        if curr_request.connection != self.__get_curr_turn_client():
            # request made from client not in turn
            # yell at the client
            curr_request.connection.send_data(
                ServerResponse(curr_request.connection.get_player().get_hand(),
                               self.__board,
                               curr_request.connection.get_player().score,
                               game_over=(not self.__active),
                               first=self.__is_first_turn()))
        # if request is discarding hand: handle here
        if curr_request.data.request_type == 'discard':
            # Check if discarding is valid
            valid_discard = True
            # if valid:
            if valid_discard:
                pass
                # remove tiles from hand and put back in bag
                # then call self.__start_next_turn()
            # else: yell at client
            else:
                curr_request.connection.send_data(
                    ServerResponse(
                        curr_request.connection.get_player().get_hand(),
                        self.__board,
                        curr_request.connection.get_player().score,
                        start_turn=True,
                        game_over=(not self.__active),
                        first=self.__is_first_turn()))
        # if request is placing tiles:
        elif curr_request.data.request_type == 'placement':
            # Check if placements are valid
            valid_placement = True
            for placement in curr_request:
                valid_placement = self.__gamerules.verify_move(curr_request)
                if not valid_placement:
                    break
            # if placements are valid:
            if valid_placement:
                # update score of current player
                self.__curr_player.score += self.__gamerules.score_move(curr_request)
                # mark placed tiles as permanent using Tile.set_permanent()
                # then add the tiles to the board
                for placement in curr_request.data:
                    placement.tile.set_permanent()
                    self.__board.get_board()[placement.x_coord, placement.y_coord] = placement.tile
                # then call self.__start_next_turn()
                self.__start_next_turn()
            else:
                # yell at client
                curr_request.connection.send_data(
                    ServerResponse(
                        curr_request.connection.get_player().get_hand(),
                        self.__board,
                        curr_request.connection.get_player().score,
                        start_turn=True,
                        game_over=(not self.__active),
                        first=self.__is_first_turn()))
        # else:
        else:
            # this means that request is invalid, so yell at client
            curr_request.connection.send_data(
                ServerResponse(curr_request.connection.get_player().get_hand(),
                               self.__board,
                               curr_request.connection.get_player().score,
                               start_turn=True,
                               game_over=(not self.__active),
                               first=self.__is_first_turn()))

    def sync_all_players(self):
        """Synchronizes all player states
        """
        for i in range(len(self.__clients)):
            self.__clients[i].send_data(
                ServerResponse(self.__clients[i].get_player().get_hand(),
                               self.__board,
                               self.__clients[i].get_player().score,
                               valid=True,
                               start_turn=(i == self.__curr_player),
                               game_over=(not self.__active),
                               winner=(i == self.__winner()),
                               first=self.__is_first_turn()))

    def __winner(self) -> int:
        if not self.__active:
            # TODO: Check this
            NotImplemented
        return -1

    def __is_first_turn(self):
        for client in self.__clients:
            if client.get_player().score != 0:
                return False
        return True

    def __get_curr_turn_client(self):
        """Gets client playing the turn.
        """
        return self.__clients[self.__curr_player]

    def __start_next_turn(self):
        """Starts next turn
        """
        for i in range(6):
            if self.__get_curr_turn_client().get_player()[i] is None:
                self.__get_curr_turn_client().get_player(
                )[i] = self.__tile_bag.pop(rand.randrange(len(self.__tile_bag)))
        # check if game is over (i.e., no more tiles can be placed)
        # if game over:
        # set self.__active to false
        self.__curr_player = (self.__curr_player + 1) % len(self.__clients)
        self.sync_all_players()

    def has_request(self):
        """Checks whether there is request to process

        Returns:
            True if there is >=1 request to process
        """
        return not self.__requests.empty()

    def in_game(self):
        """Checks current state of game

        Returns:
            True if game is running.
        """
        return self.__active
