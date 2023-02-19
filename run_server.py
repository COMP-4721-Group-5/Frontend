#!/usr/bin/python3

import socket
from queue import Queue
import random as rand
from typing import List

from lib.backend.server_components import *


sock = server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
sock.bind(("", 1234))
sock.listen()

connections: List[ClientConnection] = list()
request_queue: Queue[Request] = Queue()

for i in range(2): # Arbitrary limitation of 2 players for POC
    csock, addr = sock.accept()
    connections.append(ClientConnection(csock, addr, request_queue))

sock.close()

game_controller = QwirkeleController(connections, request_queue)

while game_controller.in_game():
    try:
        game_controller.process_request()
    except KeyboardInterrupt:
        break

# TODO: Cleanup / Close
