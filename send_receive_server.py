import select
from socket import *
from server.server import *
from db.db import *




db_conn = db()
conn_sock = socket(AF_INET,SOCK_STREAM)
conn_sock.bind(("localhost",50002))
conn_sock.listen(5)
lst = []
lst.append(conn_sock)
server = server(conn_sock,lst,{},{},db_conn)
server.recv_msgs()