import threading
import socket
import logging

from .classes import *

global packets_sent
packets_sent = 0

def func(conn, addr, conn_data: Connection):
    global packets_sent
    logging.info(f"Connection from {addr[0]}:{addr[1]}")
    data = conn.recv(1024)
    packets = conn_data.parse_packets(data)
    for i in packets:
        logging.debug(f"Packet {packets_sent}: {i.raw_data}")
        packets_sent += 1
    conn.close()

server = Connection("Server", 25565)
server.Start(func)