#!/usr/bin/python3

import socket
from queue import Queue
import random as rand
from typing import List

from lib.backend.server_components import *
from lib.shared.internal_structures import Board
from lib.shared.internal_structures import Tile
from lib.shared.internal_structures import TileColor
from lib.shared.internal_structures import TileShape


sock = server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
sock.bind(("", 1234))
sock.listen()

connections: List[ClientConnection] = list()
request_queue: Queue[Request] = Queue()

for i in range(2): # Arbitrary limitation of 2 players for POC
    csock, addr = sock.accept()
    connections.append(ClientConnection(csock, addr, request_queue))


sock.close()

# TODO: Initialize game

game_board = Board()

tile_bag: List[Tile] = list()

for i in range(3):
    for color in TileColor:
        for shape in TileShape:
            tile_bag.append(Tile(color, shape))

for client in connections:
    for i in range(6):
        # Add tiles to player
        # TODO: Initialize underlying hand list inside Player
        client.get_player()[i] = tile_bag.pop(rand.randrange(len(tile_bag)))

# TODO: Sync Initialization state with all clients

# TODO: Initialize request processor

while True: # TODO: eplace with game state conditional
    try:
        pass
    except KeyboardInterrupt:
        break

# TODO: Cleanup / Close
