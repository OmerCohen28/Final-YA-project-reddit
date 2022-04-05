from user.user import *
from db.db import *
from socket import *
from chatroom.chatroom import *

sock = socket(AF_INET,SOCK_STREAM)
sock.bind(("",50001))

sock.connect("",50000)

msgs = ["new user","omer","1234","20",False]

for msg in msgs:
    sock.send(msg.encode())
    lol = pickle.loads(sock.recv(1054))
    print(lol)
