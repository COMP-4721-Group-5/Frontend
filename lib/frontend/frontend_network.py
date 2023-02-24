import json
from typing import Final
import socket
from threading import Event
from threading import Thread

from pygame import USEREVENT
import pygame.event

from ..shared.network_exchange_format import JsonableEncoder
from ..shared.network_exchange_format import JsonableDecoder
from ..shared.network_exchange_format import ClientRequest
from ..shared.network_exchange_format import ServerResponse


class DataReceivedEvent(pygame.event.Event):
    """Custom Pygame Event for Data Received
    
    Provides customized Pygame event that gets
    added to the event queue when some data is
    received from the server over the network.

    Attributes:
        valid: Flag for validity of latest request
        curr_hand: Current state of the hand of the player
        curr_board: Current state of the board
        curr_score: Current score of the player
    """
    EVENTTYPE: Final[int] = USEREVENT + 1

    def __init__(self, data: ServerResponse):
        super().__init__(DataReceivedEvent.TYPE, data.json_serialize())


class ClientSocket:
    """Python Implementation of Client socket.
    
    Provides implementation of network socket the
    client needs for communicating with the server.

    Attributes:
        host: Address of the host (server)
        port: Port number to connect to
        sock: low-level socket object connected to host
        closed: Flag indicating status of socket
    """

    __host: str
    __port: int
    __sock: socket.socket
    __closed: Event
    __listener: '_ServerMsgListener'

    def __init__(self, host: str, port: int) -> None:
        """Initializes the socket instance

        Args:
            host: Address of the host (server)
            port: Port number to connect to
        """
        self.__host = host
        self.__port = port
        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__sock.connect((self.__host, self.__port))
        self.__listener = ClientSocket._ServerMsgListener(self)
        self.__closed = Event()
        self.__listener.start()

    def send_data(self, data: ClientRequest) -> None:
        """Sends given data to the connected host.

        Args:
            data: data to send to the host
        """
        self.__sock.send(json.dumps(data, cls=JsonableEncoder).encode())

    def close(self) -> None:
        """Closes connection with the server.
        """
        if self.__closed.is_set():
            return
        self.__closed.set()

    @property
    def closed(self) -> bool:
        """Flag indicating status of socket"""
        return self.__closed.is_set()

    class _ServerMsgListener(Thread):
        """Multithreaded socket listener implementation for client
        """
        __connection: 'ClientSocket'

        def __init__(self, connection: 'ClientSocket'):
            self.__connection = connection

        def run(self):
            while not self.__connection.__closed.is_set():
                recv_data = self.__connection.__sock.recv(4096)
                if len(recv_data) == 0:
                    self.__connection.close()
                response = json.loads(recv_data.decode(), cls=JsonableDecoder)
                pygame.event.post(DataReceivedEvent(response))

            self.__connection.__sock.shutdown(socket.SHUT_WR)

            while len(self.__connection.__sock.recv(1024)) != 0:
                self.__connection.__sock.send(b'')

            self.__connection.__sock.close()
