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
    "previewsChat": True,
    "enforcesSecureChat": True,
    "favicon": "data:image/png;base64,<data>"
}

global packets_sent
packets_sent = 0

def func(conn, addr, conn_data: Connection):
    global packets_sent
    logging.info(f"Connection from {addr[0]}:{addr[1]}")
    data = conn.recv(1024)
    logging.debug(f"Receved Data: {data}")
    packets = conn_data.parse_packets(data)
    for i in packets:
        logging.debug(f"Packet {packets_sent}: {i.id}, {i.data}")
        packets_sent += 1
        
        send_data = b""
        
        if i.id == 0 and i.data.__len__() == 0:
            packet = Packet()
            packet.create_packet(bytes(1), [json.dumps(info).encode("utf-8")])
            send_data += packet.raw_data
        elif i.id == 1:
            logging.debug(f"Receved ping with long {Minecraft_Long(i.data)}")
            send_data += i.raw_data
            
        
        logging.debug(f"Sending; {send_data}")
        conn.send(send_data)
        
    conn.close()

server = Connection("Server", 25565)
server.Start(func)