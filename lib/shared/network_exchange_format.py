from abc import ABC, abstractmethod
from enum import IntEnum
import json
from typing import Any, Dict, final, TypeVar

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
        else:
            return dct

