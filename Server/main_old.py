import logging

server_info = b'x\x00v{"description":{"text":"A Minecraft Server"},"players":{"max":20,"online":0},"version":{"name":"1.16","protocol":735}}'

c = ""

for i in server_info:
    c += chr(i)
logging.debug(c)


6

# first of all import the socket library
import socket 
 
output_file = open("out.txt", "wb")
output_file.write(b"") 
output_file.close
 
# next create a socket object
s = socket.socket()        
logging.info ("Socket successfully created")
# reserve a port on your computer in our
# case it is 12345 but it can be anything
port = 25565
 
# Next bind to the port
# we have not typed any ip in the ip field
# instead we have inputted an empty string
# this makes the server listen to requests
# coming from other computers on the network
s.bind(('', port))        
logging.info ("socket binded to %s" %(port))
 
# put the socket into listening mode
s.listen(5)    
logging.info ("socket is listening")           
 
# a forever loop until we interrupt it or
# an error occurs
start = False
while True:
 
# Establish connection with client.
  c, addr = s.accept()   
  output_file = open("out.txt", "ab")
  logging.info('\n\nGot connection from '+str(addr[0])+"\n")
  data_str = ""
  data = c.recv(1024)
  logging.debug(f"Receved: {data}")
  for i in data:
    data_str += chr(i)
  output_file.write(data)
  output_file.close()
  if data[0] == 16:
      send_data =str(server_info).encode("utf-8")
      c.send(send_data)
      logging.debug(f"Sending: {send_data}")
  elif data[0] == b"\t":
      # send_data = b'\xff\x00\x23\x00\xa7\x00\x31\x00\x00\x00\x34\x00\x37\x00\x00\x00\x31\x00\x2e\x00\x34\x00\x2e\x00\x32\x00\x00\x00\x41\x00\x20\x00\x4d\x00\x69\x00\x6e\x00\x65\x00\x63\x00\x72\x00\x61\x00\x66\x00\x74\x00\x20\x00\x53\x00\x65\x00\x72\x00\x76\x00\x65\x00\x72\x00\x00\x00\x30\x00\x00\x00\x32\x00\x30'
      send_data = data
      logging.debug(f"Sending: {send_data}")
      c.send(send_data)