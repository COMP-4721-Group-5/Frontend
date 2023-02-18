import socket

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

    def send_data(self, data: str):
        """Sends given data to the connected host.

        Args:
            data: data to send to the host
        
        Returns:
            Response returned by the host.
        """
        self.__sock.send(data.encode())
        recv_msg = self.__sock.recv(4096)
        if len(recv_msg) == 0:
            self.close()
        return recv_msg.decode()

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
