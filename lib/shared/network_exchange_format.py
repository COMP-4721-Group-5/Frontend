from enum import IntFlag
import json
from typing import Any, Dict, Final, List

from .internal_structures import JsonableObject
from .internal_structures import Tile
from .internal_structures import Placement
from .internal_structures import Board


class JsonableEncoder(json.JSONEncoder):
    """Custom JSON Encoder for Jsonable Objects
    """

    def default(self, o: Any) -> Any:
        if isinstance(o, JsonableObject):
            return o.json_serialize()
        return super().default(o)


class JsonableDecoder(json.JSONDecoder):
    """Custom JSON Decoder for Jsonable Objects
    """

    def __init__(self, *args, **kwargs):
        json.JSONDecoder.__init__(self,
                                  *args,
                                  object_hook=self.object_hook,
                                  **kwargs)

    def object_hook(self, dct: Dict[str, Any]):
        if 'type' in dct.keys():
            if dct['type'] == Tile.JSONABLE_TYPE:
                return Tile.json_deserialize(dct)
            elif dct['type'] == Placement.JSONABLE_TYPE:
                return Placement.json_deserialize(dct)
            elif dct['type'] == Board.JSONABLE_TYPE:
                return Board.json_deserialize(dct)
            elif dct['type'] == ClientRequest.JSONABLE_TYPE:
                return ClientRequest.json_deserialize(dct)
            elif dct['type'] == ServerResponse.JSONABLE_TYPE:
                return ServerResponse.json_deserialize(dct)
        else:
            return dct


class ClientRequest(JsonableObject):
    """Python Representation of Request from Client
    """
    JSONABLE_TYPE: Final[str] = 'request'
    __request_type: str
    __data: List[Tile] | List[Placement]

    def __init__(self, request_type: str, data: List[Placement] | List[Tile]):
        if request_type in ['discard', 'placement']:
            self.__request_type = request_type
            self.__data = data
        else:
            raise ValueError

    @property
    def request_type(self):
        return self.__request_type

    def __getitem__(self, key: int):
        return self.__hand[key]

    def __iter__(self):
        return iter(self.__data)

    def json_serialize(self) -> Dict[str, str | List[Placement] | List[Tile]]:
        dict_form = {
            'type': ClientRequest.JSONABLE_TYPE,
            'request_type': self.__request_type,
            'data': self.__data
        }
        return dict_form

    def json_deserialize(serialized_form: Dict[str, str | List[Placement] |
                                               List[Tile]]):
        new_request = ClientRequest(serialized_form['request_type'],
                                    serialized_form['data'])
        return new_request


class ServerResponse(JsonableObject):
    """Python Representation of Response from Server
    """
    JSONABLE_TYPE: Final[str] = 'response'
    __flag: 'ServerResponse.ResponseFlag'
    __curr_hand: List[Tile]
    __curr_board: Board
    __user_id: int
    __scores: int

    def __init__(self,
                 hand: List[Tile],
                 board: Board,
                 user_id: int,
                 scores: List[int],
                 valid: bool = False,
                 first: bool = False,
                 start_turn: bool = False,
                 game_over: bool = False,
                 winner: bool = False,
                 flag: int = -1) -> None:
        self.__flag = (
            (ServerResponse.ResponseFlag.VALID if valid else 0) |
            (ServerResponse.ResponseFlag.FIRST if first else 0) |
            (ServerResponse.ResponseFlag.START_TURN if start_turn else 0) |
            (ServerResponse.ResponseFlag.GAME_OVER if game_over else 0) |
            (ServerResponse.ResponseFlag.WINNER if winner else 0)
        ) if flag < 0 else ServerResponse.ResponseFlag(flag)
        self.__curr_hand = hand
        self.__curr_board = board
        self.__user_id = user_id
        self.__scores = scores

    @property
    def valid(self):
        """Indicates whether the latest request was valid.
        """
        return self.__valid

    @property
    def curr_hand(self):
        return self.__curr_hand

    @property
    def curr_board(self):
        """Gets current state of board
        """
        return self.__curr_board

    @property
    def curr_score(self):
        """Gets current score.
        """
        return self.__scores[self.__user_id]

    def json_serialize(self) -> Dict[str, List[Tile] | Board | int]:
        dict_form = {
            'type': ServerResponse.JSONABLE_TYPE,
            'flag': int(self.__flag),
            'curr_hand': self.__curr_hand,
            'curr_board': self.__curr_board,
            'user_id': self.__user_id,
            'scores': self.__scores
        }
        return dict_form

    def json_deserialize(serialized_form: Dict[str, List[Tile] | Board | int]):
        return ServerResponse(serialized_form['curr_hand'],
                              serialized_form['curr_board'],
                              serialized_form['user_id'],
                              serialized_form['scores'],
                              flag=serialized_form['flag'])

    class ResponseFlag(IntFlag):
        """Flags being used for Server Response
        
        VALID:  Indicates whether this response is valid.
                This flag should not be set when responding
                to an invalid request.
        FIRST:  Indicates whether the first tile has been placed
                on the board.
        START_TURN: Indicates whether the receiving client should
                    start its turn.
        GAME_OVER:  Indicates whether the game is over.
        WINNER: Indicates whether the receiving client is the winner
                of the game.
                This flag should NOT be set if GAME_OVER is not set.
        """
        VALID = 0b00001
        FIRST = 0b00010
        START_TURN = 0b00100
        GAME_OVER = 0b01000
        WINNER = 0b10000
