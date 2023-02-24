import json
from typing import Final
import socket

from pygame import USEREVENT
import pygame.event

from ..shared.network_exchange_format import JsonableEncoder
from ..shared.network_exchange_format import ClientRequest

class DataReceivedEvent(pygame.event.Event):
    TYPE: Final[int] = USEREVENT + 1

    def __init__(self):
        super().__init__(DataReceivedEvent.TYPE, None)
        # TODO: Replace None arg with data objects

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
    __closed: bool

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
        self.__closed = False

    def send_data(self, data: ClientRequest) -> None:
        """Sends given data to the connected host.

        Args:
            data: data to send to the host
        """
        self.__sock.send(json.dumps(data, cls = JsonableEncoder).encode())

    def close(self) -> None:
        """Closes connection with the server.
        """
        if self.__closed: return
        self.__closed = True
        self.__sock.shutdown(socket.SHUT_WR)
        while len(self.__sock.recv(1024)) != 0:
            self.__sock.send(b'')
        self.__sock.close()
    
    @property
    def closed(self) -> bool:
        """Flag indicating status of socket"""
        return self.__closed
