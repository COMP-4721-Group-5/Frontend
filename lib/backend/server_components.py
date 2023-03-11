from dataclasses import dataclass
import json
import logging
from queue import Queue
import socket
import time
from threading import Event
from threading import Thread
from typing import Tuple, TypeAlias

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
    _logger: logging.Logger

    def __init__(self, csock: socket.socket, addr: Address,
                 msg_queue: Queue[Request]) -> None:
        self._csock = csock
        self.__addr = addr
        self.__listener = ClientConnection._ClientMsgListener(self, msg_queue)
        self._stop_listen = Event()
        self.__listener.start()
        self.__player = Player()
        self._logger = logging.getLogger(str(self.__addr))

    def send_data(self, data: ServerResponse):
        """Sends data to client.

        Args:
            data: Data to send to client
        """
        self._logger.info(f'Sending message to {self.__addr}')
        self._csock.send(json.dumps(data, cls=JsonableEncoder).encode())

    def stop_listening(self) -> None:
        """Stops listening from client.
        """
        self._stop_listen.set()

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
            Thread.__init__(self,
                            name="ClientMsgListener-%s:%d" %
                            (connection.address[0], connection.address[1]))
            self.__connection = connection
            self.__msg_queue = msg_queue

        def run(self):
            while not self.__connection._stop_listen.is_set():
                recv_data = json.loads(
                    self.__connection._csock.recv(4096).decode(),
                    cls=JsonableDecoder)
                self.__connection._logger.info(
                    f'Received data from {self.__connection.address}')
                self.__msg_queue.put(
                    Request(self.__connection, time.time(), recv_data))

            self.__connection._csock.shutdown(socket.SHUT_WR)

            while len(recv_data) != 0:
                recv_data = self.__connection._csock.recv(1024)

            self.__connection._csock.close()
