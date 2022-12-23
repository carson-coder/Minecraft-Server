import threading
import socket
import logging
import json

from .classes import *

info = {
    "version": {
        "name": "1.19.3",
        "protocol": 761
    },
    "players": {
        "max": 100000000,
        "online": 1000000,
        "sample": [
            {
                "name": "thinkofdeath",
                "id": "4566e69f-c907-48ee-8d71-d7ba5aa00d20"
            }
        ]
    },
    "description": {
        "text": "Hello world"
    },
    "favicon": "data:image/png;base64,<data>",
    "previewsChat": True,
    "enforcesSecureChat": True,
}

global packets_sent
packets_sent = 0

def func(conn, addr, conn_data: Connection):
    global packets_sent
    logging.info(f"Connection from {addr[0]}:{addr[1]}")
    data = conn.recv(1024)
    packets = conn_data.parse_packets(data)
    for i in packets:
        logging.debug(f"Packet {packets_sent}: {i.data}")
        packets_sent += 1
        
        send_data = b""
        
        if i.id == 0 and i.data.__len__() == 0:
            packet = Packet()
            packet.create_packet(0, [json.dumps(info).encode("utf-8")])
            send_data += packet.raw_data
        elif i.id == 1 and len(i.items) == 1:
            send_data += i.raw_data
            
        
        logging.debug(f"Sending; {packet.raw_data}")
        conn.send(send_data)
        
    conn.close()

server = Connection("Server", 25565)
server.Start(func)