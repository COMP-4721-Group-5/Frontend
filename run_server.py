#!/usr/bin/python3

import logging
import socket
from queue import Queue
import random as rand
from typing import List

from lib.backend.server_components import *

port = 12345

logging.basicConfig(encoding='utf-8',
                    level=logging.DEBUG,
                    format='%(asctime)s %(message)s')
logging.info('Starting server...')

sock_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock_server.bind(("", port))
logging.info(f'Listening on port {port}')
sock_server.listen()

connections: List[ClientConnection] = list()
request_queue: Queue[Request] = Queue()

for i in range(2):  # Arbitrary limitation of 2 players for POC
    csock, addr = sock_server.accept()
    logging.info(f'Received connection from {addr}')
    connections.append(ClientConnection(csock, addr, request_queue))

sock_server.close()

game_controller = QwirkeleController(connections, request_queue)

while game_controller.in_game():
    try:
        game_controller.process_request()
    except KeyboardInterrupt:
        logging.critical('Ctrl+C received, exiting.')
        for connection in connections:
            connection.stop_listening()
        break
    except ConnectionError:
        logging.error('Closing all other connections.')
        for connection in connections:
            connection.stop_listening()
        logging.error('Exiting')
        break

# TODO: Cleanup / Close
