import json, socket

class ClientSocket:

    __host: str
    __port: int
    __sock: socket.socket

    def __init__(self, host: str, port: int) -> None:
        self.__host = host
        self.__port = port
        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def send_data(self, data):
        return self.__sock.sendto(data, (self.__host, self.__port))

    def receive_data(self):
        pass

    def parse_data(data: str):
        pass