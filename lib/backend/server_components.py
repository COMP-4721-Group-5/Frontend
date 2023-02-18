from dataclasses import dataclass
from queue import Queue
import socket
import time
from threading import Event
from threading import Thread
from typing import Tuple, TypeAlias

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

    def __init__(self, csock: socket.socket, addr: Address, msg_queue: Queue[Request]) -> None:
        self.__csock = csock
        self.__addr = addr
        self.__listener = ClientConnection._ClientMsgListener(self, msg_queue)
        self.__stop_listen = Event()
        self.__listener.start()
    
    def stop_listening(self) -> None:
        self.__stop_listen.set()
    
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





