from typing import Union

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
class Long(McDatatype):
    size = 8
    def __init__(self, value: Union[int, bytes]):
        if type(value) == int:
            self.value = value
        else:
            self.value = int.from_bytes(value, byteorder='big')