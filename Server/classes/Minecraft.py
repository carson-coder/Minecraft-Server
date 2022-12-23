from typing import Union

def writeVarint(value: int) -> bytes:
    byte_value = value.to_bytes(8, 'big')[::-1]
    while byte_value.endswith(b'\x00'):
        byte_value = byte_value.removesuffix(b'\x00')
    if value <= 0xfc:
        a = byte_value
    elif value <= 0xffff:
        a = b'\xfd'.join([b"",byte_value])
    elif value <= 0xffffffff:
        a = b'\xfe'.join([b"",byte_value])
    elif value <= 0xffffffffffffffff:
        a = b'\xff'.join([b"",byte_value])
    else:
        raise Exception("Value is too big")
    val = a[len(a)-1:len(a)-1] + b'\x01'
    a.removesuffix(a[len(a)-1:len(a)-1])
    a += val
    return(a)

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
        self.value

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