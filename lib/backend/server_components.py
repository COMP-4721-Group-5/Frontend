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
from ..shared.player import Player

Address: TypeAlias = Tuple[str, int]

@dataclass
class Request:
    connection: 'ClientConnection'
    time: float
    data: str

class ClientConnection:
    __csock: socket.socket
    __addr: Address
    __listener: '_ClientMsgListener'
    __stop_listen: Event
    __player: Player

    def __init__(self, csock: socket.socket, addr: Address, msg_queue: Queue[Request]) -> None:
        self.__csock = csock
        self.__addr = addr
        self.__listener = ClientConnection._ClientMsgListener(self, msg_queue)
        self.__stop_listen = Event()
        self.__listener.start()

    def send_data(self, data: str):
        self.__csock.send(data.encode())

    def stop_listening(self) -> None:
        self.__stop_listen.set()

    def get_player(self):
        return self.__player

    @property
    def address(self) -> Address:
        return self.__addr

    class _ClientMsgListener(Thread):
        __connection: 'ClientConnection'
        __msg_queue: Queue[Request]

        def __init__(self, connection: 'ClientConnection', msg_queue: Queue[Request]):
            self.__connection = connection
            self.__msg_queue = msg_queue

        def run(self):
            while not self.__connection.__stop_listen.is_set():
                recv_data = self.__connection.__csock.recv(4096).decode()
                self.__msg_queue.put(Request(self.__connection, time.time(), recv_data))

            self.__connection.__csock.shutdown(socket.SHUT_WR)

            while len(recv_data) != 0:
                recv_data = self.__connection.__csock.recv(1024)

            self.__connection.__csock.close()

class QwirkeleController:
    __clients: List[ClientConnection]
    __requests: Queue[Request]
    __board: Board
    __tile_bag: List[Tile]
    __active: bool
    __curr_player: int

    def __init__(self, client_list: List[ClientConnection], request_queue: Queue[Request]) -> None:
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
                # TODO: Initialize underlying hand list inside Player
                client.get_player()[i] = self.__tile_bag.pop(rand.randrange(len(self.__tile_bag)))
        self.sync_all_players()
        self.__start_next_turn()

    def process_request(self):
        curr_request = self.__requests.get()
        parsed_request = json.loads(curr_request.data, cls = JsonableDecoder)
        if curr_request.connection != self.__get_curr_turn_client():
            # request made from client not in turn
            # yell at the client
            pass
        # if request is discarding hand: handle here
            # Check if discarding is valid
            # if valid:
                # remove tiles from hand and put back in bag
                # then call self.__start_next_turn()
            # else: yell at client
        # if request is placing tiles:
            # Check if placements are valid
            # if placements are valid:
                # mark placed tiles as permanent using Tile.set_permanent()
                # update score of current player
                # then call self.__start_next_turn()
        # else:
            # this means that request is invalid, so yell at client

    def sync_all_players(self):
        for client in self.__clients:
            # send current board state to client
            # send current player state to client
            pass

    def __get_curr_turn_client(self):
        return self.__clients[self.__curr_player]

    def __start_next_turn(self):
        for i in range(6):
            if self.__get_curr_turn_client()[i] is None:
                self.__get_curr_turn_client()[i] = self.__tile_bag.pop(rand.randrange(len(self.__tile_bag)))
        self.sync_all_players()
        self.__curr_player = (self.__curr_player + 1) % len(self.__clients)
        # check if game is over (i.e., no more tiles can be placed)
        # if game over:
            # set self.__active to false
            # announce game over
        # else:
            # Message next client to start turn

    def has_request(self):
        return not self.__requests.empty()

    def in_game(self):
        return self.__active
