from dataclasses import dataclass
import json
from queue import Queue
import random as rand
import socket
import time
from threading import Event
from threading import Thread
from typing import List, Tuple, TypeAlias

from ..shared.internal_structures import Board
from ..shared.internal_structures import Tile
from ..shared.internal_structures import TileColor
from ..shared.internal_structures import TileShape
from ..shared.network_exchange_format import JsonableDecoder
from ..shared.network_exchange_format import JsonableEncoder
from ..shared.network_exchange_format import ClientRequest
from ..shared.network_exchange_format import ServerResponse
from ..shared.player import Player

Address: TypeAlias = Tuple[str, int]


@dataclass
class Request:
    """Python Representation of Received Request

    Attributes:
        connection: Connection to a client
        time: Time of request
        data: Content of request
    """
    connection: 'ClientConnection'
    time: float
    data: ClientRequest


class ClientConnection:
    """Python Representation of Connection to a Client
    """
    _csock: socket.socket
    __addr: Address
    __listener: '_ClientMsgListener'
    _stop_listen: Event
    __player: Player

    def __init__(self, csock: socket.socket, addr: Address,
                 msg_queue: Queue[Request]) -> None:
        self._csock = csock
        self.__addr = addr
        self.__listener = ClientConnection._ClientMsgListener(self, msg_queue)
        self._stop_listen = Event()
        self.__listener.start()
        self.__player = Player()

    def send_data(self, data: ServerResponse):
        """Sends data to client.

        Args:
            data: Data to send to client
        """
        self._csock.send(json.dumps(data, cls=JsonableEncoder).encode())

    def stop_listening(self) -> None:
        """Stops listening from client.
        """
        self._stop_listen.set()
        self._csock.settimeout(0)

    def get_player(self):
        """Gets underlying player data for this client.

        Returns:
            Underlying player data for this client.
        """
        return self.__player

    @property
    def address(self) -> Address:
        """Gets address of the client.
        """
        return self.__addr

    class _ClientMsgListener(Thread):
        """Multithreaded socket listener implementation for server
        """
        __connection: 'ClientConnection'
        __msg_queue: Queue[Request]

        def __init__(self, connection: 'ClientConnection',
                     msg_queue: Queue[Request]):
            Thread.__init__(self)
            self.__connection = connection
            self.__msg_queue = msg_queue

        def run(self):
            self.__connection._csock.settimeout(0)
            recv_data = bytes()
            while not self.__connection._stop_listen.is_set():
                try:
                    recv_data = json.loads(
                    self.__connection._csock.recv(4096).decode(),
                    cls=JsonableDecoder)
                except:
                    pass
                if len(recv_data) != 0:
                    self.__msg_queue.put(
                        Request(self.__connection, time.time(), recv_data))

            self.__connection._csock.shutdown(socket.SHUT_WR)

            while len(recv_data) != 0:
                recv_data = self.__connection._csock.recv(1024)

            self.__connection._csock.close()


class QwirkeleController:
    """Root controller for Qwirkle Server

    Attributes:
        clients: Clients connected to this server
        requests: Queue of requests from clients
        board: Internal board instance
        tile_bag: Bag of tiles
        active: Indicates current state of server
        curr_player: Current player in turn
    """
    __clients: List[ClientConnection]
    __requests: Queue[Request]
    __board: Board
    __tile_bag: List[Tile]
    __active: bool
    __curr_player: int

    def __init__(self, client_list: List[ClientConnection],
                 request_queue: Queue[Request]) -> None:
        self.__clients = client_list
        self.__requests = request_queue
        self.__curr_player = 0
        self.__active = True
        self.__board = Board()
        self.__tile_bag = list()
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
                               curr_request.connection.get_player().__score,
                               flag=0b0000))
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
                        curr_request.connection.get_player().__score,
                        flag=0b0000))
        # if request is placing tiles:
        elif curr_request.data.request_type == 'placement':
            # Check if placements are valid
            valid_placement = True
            # if placements are valid:
            if valid_placement:
                pass
                # mark placed tiles as permanent using Tile.set_permanent()
                # update score of current player
                # then call self.__start_next_turn()
            else:
                # yell at client
                curr_request.connection.send_data(
                    ServerResponse(
                        curr_request.connection.get_player().get_hand(),
                        self.__board,
                        curr_request.connection.get_player().__score,
                        flag=0b0000))
        # else:
        else:
            # this means that request is invalid, so yell at client
            curr_request.connection.send_data(
                ServerResponse(curr_request.connection.get_player().get_hand(),
                               self.__board,
                               curr_request.connection.get_player().__score,
                               flag=0b0000))

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
