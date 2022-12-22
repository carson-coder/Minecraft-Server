import socket
import threading
import logging

logging.info("Running Data Logger")

listen_port = 25565
out_port = 8080

ip = "localhost"

s = socket.socket()

#Start server for minecraft to connect on
s.bind(('', listen_port))

s.listen(5)

def Listen_Client(conn, client):
    a = True
    while a:
        try:
            data = conn.recv(1024)
            data = data.replace(b"localhost", ip.encode("utf-8"))
            client.send(data)
            if data != b'':
                logging.debug(f"Minecraft: {repr(data)}")
        except Exception as e:
            logging.info("Stoping")
            logging.debug(f"Reason For Stoping\n{e}")
            a = False
            return
            
def Listen_Server(conn, client):
    a = True
    while a:
        try:
            data = client.recv(1024)
            data = data.replace(b"localhost", ip.encode("utf-8"))
            conn.send(data)
            if data != b'':
                logging.debug(f"Server   : {repr(data)}")
        except Exception as e:
            logging.info("Stoping")
            logging.debug(f"Reason For Stoping\n{e}")
            a = False
            return

def retrue():
    return(True)
con = retrue
while con():
    conn, addr = s.accept()
    logging.info("Connection From Minecraft.")
    cs = socket.socket()
    cs.connect((socket.gethostbyname(ip) , out_port))
    logging.info("Connected To Server")
    sl = threading.Thread(target=Listen_Server, args=(conn, cs))
    cl = threading.Thread(target=Listen_Client, args=(conn, cs))
    sl.start()
    cl.start()
    sl.name = "Server>Client Thread"
    cl.name = "Client>Server Thread"
    con = cl.is_alive