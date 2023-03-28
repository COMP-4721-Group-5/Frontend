import json
from typing import Final, final, NoReturn
import socket
from threading import Event
from threading import Thread

from pygame import USEREVENT
import pygame.event

from ..shared.network_exchange_format import JsonableEncoder
from ..shared.network_exchange_format import JsonableDecoder
from ..shared.network_exchange_format import ClientRequest
from ..shared.network_exchange_format import ServerResponse


@final
class DataReceivedEvent:
    """Utility class for creating custom Pygame events when data is received.

    Do not instantiate object of this type.
    """

    EVENTTYPE: Final[int] = USEREVENT + 1

    def __init__(self) -> NoReturn:
        raise NotImplementedError

    @staticmethod
    def create_event(data: ServerResponse):
        amended_data = data.json_serialize()
        amended_data.pop("type")
        amended_data["flag"] = ServerResponse.ResponseFlag(amended_data["flag"])
        return pygame.event.Event(DataReceivedEvent.EVENTTYPE, amended_data)


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
    _sock: socket.socket
    _closed: Event
    __listener: "_ServerMsgListener"

    def __init__(self, host: str, port: int) -> None:
        """Initializes the socket instance

        Args:
            host: Address of the host (server)
            port: Port number to connect to
        """
        self.__host = host
        self.__port = port
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sock.connect((self.__host, self.__port))
        self.__listener = ClientSocket._ServerMsgListener(self)
        self._closed = Event()
        self.__listener.start()

    def send_data(self, data: ClientRequest) -> None:
        """Sends given data to the connected host.

        Args:
            data: data to send to the host
        """
        self._sock.send(json.dumps(data, cls=JsonableEncoder).encode())

    def close(self) -> None:
        """Closes connection with the server."""
        if self._closed.is_set():
            return
        self._closed.set()

    @property
    def closed(self) -> bool:
        """Flag indicating status of socket"""
        return self._closed.is_set()

    class _ServerMsgListener(Thread):
        """Multithreaded socket listener implementation for client"""

        __connection: "ClientSocket"

        def __init__(self, connection: "ClientSocket"):
            Thread.__init__(
                self,
                name="ServerMsgListener-%s:%d" % (connection.address, connection.port),
            )
            self.__connection = connection

        def run(self):
            self.__connection._sock.settimeout(0)
            recv_data = None
            while not self.__connection._closed.is_set():
                try:
                    recv_data = self.__connection._sock.recv(4096)
                except:
                    pass
                if recv_data is None:
                    pass
                elif len(recv_data) != 0:
                    response = json.loads(recv_data.decode(), cls=JsonableDecoder)
                    pygame.event.post(DataReceivedEvent.create_event(response))
                    recv_data = None
                else:
                    self.__connection.close()
                    recv_data = None

            self.__connection._sock.shutdown(socket.SHUT_WR)
            self.__connection._sock.close()

    @property
    def address(self):
        """Address of the host server"""
        return self.__host

    @property
    def port(self):
        """Port being used on host server"""
        return self.__port
