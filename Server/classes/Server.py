import logging
import socket
import threading
import struct


class Packet():
    def __init__(self, data: bytes):
        self.id = data[1]
        self.data = data[2:]
        self.raw_data = data
    def __len__(self):
        self.raw_data[0]


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
        while len(data) != 0 and len(data) - 1 >= data[0]:
            packet_data = data[0:data[0]+1]
            data = data.replace(packet_data, b"")
            packets.append(Packet(packet_data))
        return(packets)
def listen(Connection: Connection, on_connection):
    while Connection.running:
        conn, addr = Connection.socket.accept()
        try:
            on_connection(conn, addr, Connection)
        except Exception as e:
            #logging.error(f"Error while running on_connection function: {e}")
            raise e