import socket

class ClientSocket:
    """Python Implementation of Client socket.
    
    Provides implementation of network socket the
    client needs for communicating with the server.

    Attributes:
        host: Address of the host (server)
        port: Port number to connect to
        sock: low-level socket object connected to host
    """

    __host: str
    __port: int
    __sock: socket.socket

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

    def send_data(self, data: str):
        """Sends given data to the connected host.

        Args:
            data: data to send to the host
        
        Returns:
            Response returned by the host.
        """
        self.__sock.send(data.encode())
        return self.__sock.recv(4096).decode()

    def close(self) -> None:
        """Closes connection with the server.
        """
        self.__sock.close()
