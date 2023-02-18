#!/usr/bin/python3

import socket
from queue import Queue
from typing import List

from lib.backend.server_components import *

sock = server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
sock.bind(("", 1234))
sock.listen()

connections: List[ClientConnection] = list()
request_queue: Queue[Request] = Queue()

for i in range(2):
    csock, addr = sock.accept()
    connections.append(ClientConnection(csock, addr, request_queue))
    

