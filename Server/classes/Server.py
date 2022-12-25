import logging
import socket
import threading
import io

def get_varint(data: bytes) -> bytes:
    if type(data) == int:
        data = data.to_bytes(8, "big")
    keys = {
        0xfd: 2,
        0xfe:  4,
        0xff:  8
    }
    if data[0] < 0xfd:
        return(data[0:1])
    elif data[0] in keys.keys():
        return(data[0:keys[data[0]]+1])
    else:
        raise Exception("Something happened. This should not run")

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
    
def read_varint(val: bytes, auto_get_varint=True) -> int:
    if auto_get_varint:
        val = get_varint(val)
    value = int.from_bytes(val,"big")
    a = 0
    if value <= 0xfc:
        a = (val[0])
    elif value <= 0xffff:
        a = (val[1:5])
    elif value <= 0xffffffff:
        a = (val[1:9])
    elif value <= 0xffffffffffffffff:
        a = (val[1:17])
    else:
        raise Exception(f"Varint { value } is too big")
    if type(a) == int:
        a = a.to_bytes(4, "little")
    a = int.from_bytes(a, "little")
    return(a)

class Packet():
    def create_packet(self, id: bytes, data: list[bytes]):
        data_good = b""
        for i in data: 
            data_good += bytes(i)
        self.id = id
        self.data = data_good
        data_good = id + data_good
        data_good = writeVarint(len(data_good)) + data_good
        self.items = data
        self.raw_data = data_good
        return(data_good)
    def load_packet(self, data: bytes):
        logging.debug(f"Filling out packet with data {data}")
        self.raw_data = data
        self.size = read_varint(data)
        data = data.replace(get_varint(data), bytes(0))
        self.id = read_varint(data)
        data = data.replace(get_varint(data), bytes(0))
        self.data = data
    def __len__(self):
        return(self.size)


class Connection():
    def __init__(self, name, port):
        self.port = port
        self.running = False
        self.name = name
    def Start(self, on_connection):
        if self.running == False:
            self.socket = socket.socket()
            self.running = True
            self.socket.bind(('', self.port))
            self.socket.listen(5)
            self.Thread = threading.Thread(target=listen, args=(self, on_connection, ))
            self.Thread.start()
        else:
            logging.error(f"Connection already started on port {self.port}")
    def parse_packets(self, packet: bytes) -> list[Packet]:
        packets = []
        raw_data = packet
        data = packet
        size = 1
        varint_keys = {
            b"\xfd": 2,
            b"\xfe": 4,
            b"\xff": 8,
        }
        if data[0] in varint_keys.keys():
            size = data[varint_keys[data[0]]]
        while len(data) != 0 and len(data) - (size) >= read_varint(data):
            packet_length = read_varint(data)+1
            logging.debug(f"Getting 0:{packet_length} from {data}")
            packet_data = data[0:packet_length]
            data = data.replace(packet_data, b"")
            parsed_data = Packet()
            parsed_data.load_packet(packet_data)
            packets.append(parsed_data)
        return(packets)
def listen(Connection: Connection, on_connection):
    while Connection.running:
        conn, addr = Connection.socket.accept()
        try:
            on_connection(conn, addr, Connection)
        except Exception as e:
            #logging.error(f"Error while running on_connection function: {e}")
            raise e