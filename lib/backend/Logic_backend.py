import logging
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
from ..shared.player import Player
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
    __logger: logging.Logger

    def __init__(self, client_list: List[ClientConnection],
                 request_queue: Queue[Request]) -> None:
        self.__clients = client_list
        self.__requests = request_queue
        self.__curr_player = 0
        self.__active = True
        self.__board = Board()
        self.__tile_bag = list()
        self.__gamerules = Gamerules()
        self.__logger = logging.getLogger('QuirkleController')
        for i in range(3):
            for color in TileColor:
                for shape in TileShape:
                    self.__tile_bag.append(Tile(color, shape))
        for client in self.__clients:
            for i in range(6):
                # Add tiles to player
                client.get_player()[i] = self.__tile_bag.pop(
                    rand.randrange(len(self.__tile_bag)))
        self.__logger.info('Generated initial set of hands')
        self.sync_all_players()

    def process_request(self):
        """Processes a request from client
        """
        while self.__requests.empty():
            for client in self.__clients:
                if not client.listening:
                    raise ConnectionError

        curr_request = self.__requests.get()
        # use curr_request.data to access the content of request directly
        if curr_request.connection != self.__get_curr_turn_client():
            # request made from client not in turn
            # yell at the client
            self.__logger.error(
                f'Invalid request from {curr_request.connection.address}: Not this client\'s turn'
            )
            curr_request.connection.send_data(
                ServerResponse(curr_request.connection.get_player().get_hand(),
                               self.__board,
                               self.__clients.index(curr_request.connection),
                               self.__scores(),
                               game_over=(not self.__active),
                               first=self.__is_first_turn()))
        # if request is discarding hand: handle here
        if curr_request.data.request_type == 'discard':
            # Check if discarding is valid
            discard_tiles: List[Tile] = list(curr_request.data.__iter__())
            valid_discard = QwirkeleController.is_valid_discard(
                curr_request.connection.get_player(), discard_tiles)
            # if valid:
            if valid_discard:
                self.__logger.info(
                    f'Valid discard request from {curr_request.connection.address}'
                )
                # remove tiles from hand and put back in bag
                for i in range(len(discard_tiles)):
                    for j in range(6):
                        if curr_request.connection.get_player(
                        )[j] == discard_tiles[i]:
                            self.__tile_bag.append(
                                curr_request.connection.get_player()[j])
                            curr_request.connection.get_player()[j] = None
                            break
                # then call self.__start_next_turn()
                self.__start_next_turn()

            # else: yell at client
            else:
                self.__logger.error(
                    f'Invalid discard request from {curr_request.connection.address}'
                )
                curr_request.connection.send_data(
                    ServerResponse(
                        curr_request.connection.get_player().get_hand(),
                        self.__board,
                        self.__clients.index(curr_request.connection),
                        self.__scores(),
                        start_turn=True,
                        game_over=(not self.__active),
                        first=self.__is_first_turn()))
        # if request is placing tiles:
        elif curr_request.data.request_type == 'placement':
            # Check if placements are valid
            valid_placement = True
            valid_placement = self.__gamerules.verify_move(curr_request.data, self.__board)
            # if placements are valid:
            if valid_placement:
                self.__logger.info(
                    f'Valid placement request from {curr_request.connection.address}'
                )

                # update score of current player
                self.__get_curr_turn_client().get_player().score += self.__gamerules.score_move(
                    curr_request.data, self.__board)
                # mark placed tiles as permanent using Tile.set_permanent()
                # then add the tiles to the board
                for placement in curr_request.data:
                    placement.tile.set_permanent()
                    self.__board.get_board()[placement.x_coord,
                                             placement.y_coord] = placement.tile
                # then call self.__start_next_turn()
                self.__start_next_turn()
            else:
                self.__logger.error(
                    f'Invalid placement request from {curr_request.connection.address}'
                )
                # yell at client
                curr_request.connection.send_data(
                    ServerResponse(
                        curr_request.connection.get_player().get_hand(),
                        self.__board,
                        self.__clients.index(curr_request.connection),
                        self.__scores(),
                        start_turn=True,
                        game_over=(not self.__active),
                        first=self.__is_first_turn()))
        # else:
        else:
            self.__logger.error(
                f'Invalid request from {curr_request.connection.address}: Unrecognized type'
            )
            # this means that request is invalid, so yell at client
            curr_request.connection.send_data(
                ServerResponse(curr_request.connection.get_player().get_hand(),
                               self.__board,
                               self.__clients.index(curr_request.connection),
                               self.__scores(),
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
                               i,
                               self.__scores(),
                               valid=True,
                               start_turn=(i == self.__curr_player),
                               game_over=(not self.__active),
                               winner=(i == self.__winner()),
                               first=self.__is_first_turn()))

    def __scores(self) -> List[int]:
        scores = list()
        for client in self.__clients:
            scores.append(client.get_player().score)
        return scores

    def __winner(self) -> int:
        if not self.__active:
            # TODO: Check this
            NotImplemented
        return -1

    @staticmethod
    def is_valid_discard(player: Player, discard_tiles: List[Tile]):
        if len(discard_tiles) == 0:
            return False
        elif len(discard_tiles) > 6:
            return False
        hand_stat = dict()
        discard_stat = dict()
        for i in range(6):
            if player[i].hex_value in hand_stat:
                hand_stat[player[i].hex_value] += 1
            else:
                hand_stat[player[i].hex_value] = 1
        for discard in discard_tiles:
            if discard.hex_value in discard_stat:
                discard_stat[discard.hex_value] += 1
            else:
                discard_stat[discard.hex_value] = 1
        for discard_type in discard_stat.keys():
            if discard_type not in hand_stat.keys():
                return False
            elif discard_stat[discard_type] > hand_stat[discard_type]:
                return False
        return True

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
        if len(self.__tile_bag
              ) == 0:  #only checks for game over if bag is empty
            players = list()
            for client in self.__clients:
                players.append(client.get_player)
            if self.__gamerules.game_over(players, self.__board):
                self.__active = False
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
