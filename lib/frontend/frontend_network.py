import socket

class ClientSocket:

    __host: str
    __port: int
    __sock: socket.socket

    def __init__(self, host: str, port: int) -> None:
        self.__host = host
        self.__port = port
        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__sock.connect((self.__host, self.__port))

    def send_data(self, data: str):
        self.__sock.send(data.encode())
        return self.__sock.recv(4096).decode()

    def close(self) -> None:
        self.__sock.close()
