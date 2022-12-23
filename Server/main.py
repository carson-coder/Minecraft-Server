import threading
import socket
import logging
import json

from .classes import *

info = {
    "enforcesSecureChat":True,
    "description":{
        "text":"A Minecraft Server"
    },
    "players":{
        "max":1,
        "online":10000000
    },
    "version":{
        "name":"0.0.0",
        "protocol":761
    }
}

def func(conn, addr, conn_data: Connection):
    packets_sent = 1
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
        size = len(send_data)
        conn.send(send_data)
        
    conn.close()

server = Connection("Server", 25565)
server.Start(func)