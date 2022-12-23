import logging
import socket
import threading
import varint


class Packet():
    def create_packet(self, id: int, data: list[bytes]):
        data_good = b""
        for i in data:
            data_good += varint.encode(len(i))
            data_good += i
        self.id = id
        self.data = data_good
        data_good = id.to_bytes(1, "little") + data_good
        data_good = varint.encode(len(data_good)) + data_good
        self.items = data
        self.raw_data = data_good
        return(data_good)
    def load_packet(self, data: bytes):
        logging.debug(f"Filling out packet with data {data}")
        varint_keys = {
            b"\xfd": 2,
            b"\xfe": 3,
            b"\xff": 4,
        }
        if data[0] in varint_keys.keys():
            self.id = data[varint_keys[data[0]]]
            self.data = data.replace(data[:varint_keys[data[0]]+1], b"")
            self.size = varint.decode_bytes(data[0:varint_keys[data[0]]])
        else:
            self.id = data[1]
            self.data = data.replace(data[:2], b"")
            self.size = data[0]
        self.items = []
        data_temp = self.data
        # TODO: System to put all the data in a packet in a list
        # size = 1
        # if data[0] in varint_keys.keys():
        #     size = data[varint_keys[data[0]]]
        # while len(data_temp) != 0 and len(data_temp) - (size) >= varint.decode_bytes(bytes(1) + data_temp[0:size]):
        #     d = data_temp[0:varint.decode_bytes(bytes(1) + data_temp[0:size])+1]
        #     logging.debug(f"\n0:{varint.decode_bytes(data_temp[0:size] + bytes(1))+1}\n{d}\n{ data_temp[0:size]}")
        #     self.items.append(d)
        #     data_temp.replace(d, b'')
        self.raw_data = data
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
        size = 0
        varint_keys = {
            b"\xfd": 1,
            b"\xfe": 2,
            b"\xff": 3,
        }
        if data[0] in varint_keys.keys():
            size = data[varint_keys[data[0]]]
        while len(data) != 0 and len(data) - (size+1) >= varint.decode_bytes(data[0:size+1]):
            varint_length = varint.decode_bytes(data[0:size+1])
            packet_length = varint.decode_bytes(data[0:varint_length])+1
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