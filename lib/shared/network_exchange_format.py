from abc import ABC, abstractmethod
from enum import IntEnum
import json
from typing import Any, Dict, final, List, TypeVar

from .internal_structures import JsonableObject
from .internal_structures import Tile
from .internal_structures import Placement
from .internal_structures import Board

class JsonableEncoder(json.JSONEncoder):
    def default(self, o: Any) -> Any:
        if isinstance(o, JsonableObject):
            return o.json_serialize()
        return super().default(o)

class JsonableDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        json.JSONDecoder.__init__(self, *args, object_hook=self.object_hook, **kwargs)

    def object_hook(self, dct: Dict[str, Any]):
        if 'type' in dct.keys():
            if dct['type'] == 'tile':
                return Tile.json_deserialize(dct)
            elif dct['type'] == 'placement':
                return Placement.json_deserialize(dct)
            elif dct['type'] == 'board':
                return Board.json_deserialize(dct)
            elif dct['type'] == 'request':
                return ClientRequest.json_deserialize(dct)
        else:
            return dct

class ClientRequest(JsonableObject):
    __request_type: str
    __data: List[Tile] | List[Placement]

    def __init__(self, request_type: str, data: List[Placement] | List[Tile]):
        if request_type in ['discard', 'placement']:
            self.__request_type = request_type
            self.__data = data
        else:
            raise ValueError

    def json_serialize(self) -> Dict[str, str | List[Placement] | List[Tile]]:
        dict_form = {
            'type': 'request',
            'request_type': self.__request_type,
            'data': self.__data
        }
        return dict_form
    
    def json_deserialize(serialized_form: Dict[str, str | List[Placement] | List[Tile]]):
        new_request = ClientRequest(serialized_form['request_type'], serialized_form['data'])
        return new_request

