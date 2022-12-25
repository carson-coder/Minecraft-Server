from typing import Union
import logging

def writeVarint(value: int) -> bytes:
    byte_value_unshift = value.to_bytes(8, 'big')[::-1]
    while byte_value_unshift.endswith(b'\x00'):
        byte_value_unshift = byte_value_unshift.removesuffix(b'\x00')
    byte_value = byte_value_unshift
    size = byte_value.__len__()
    keys = [
        [b'', 0],
        [b'', 0],
        [b'\xfd', 2-2],
        [b'\xfe', 4-3],
        [b'\xfe', 4-4],
        [b'\xff', 8-5],
        [b'\xff', 8-6],
        [b'\xff', 8-7],
        [b'\xff', 8-8],
    ]
    byte_value = byte_value + bytes(keys[size][1])
    return(keys[size][0] + byte_value + b'\x01')

class McDatatype():
    def __str__(self) -> int:
        return(str(self.value))
    def __sizeof__(self) -> int:
        return(self.size)
    def __eq__(self, __o: object) -> bool:
        if type(__o) == McDatatype:
            return(True)
        if type(__o) == type(self) and __o.value == self.value:
            return(True)
        return(False)
    
class String(McDatatype):
    def __init__(self, value: str):
        self.value = writeVarint(len(value)) + value.encode("utf-8")
    def __bytes__(self):
        return(self.value)

class UUID(McDatatype):
    pass

class Position(McDatatype):
    pass

class Player(McDatatype):
    def __init__(self, name: String, uuid: UUID, pos: Position):
        self.name = name
        self.uuid = uuid
        self.pos = [100,100,100]
        self.value = f"Player. Name; {self.name}, UUID: {self.uuid}"

class Long(McDatatype):
    size = 8
    def __init__(self, value: Union[int, bytes]):
        if type(value) == int:
            self.value = value
        else:
            self.value = int.from_bytes(value, byteorder='big')