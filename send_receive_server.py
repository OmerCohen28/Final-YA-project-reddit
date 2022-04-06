from fileinput import fileno
import select
from socket import *
from server.server import *
from db.db import *




db_conn = db()
conn_sock = socket(AF_INET,SOCK_STREAM)
conn_sock.bind(("localhost",50000))
conn_sock.listen(5)
lst = []
lst.append(conn_sock)
sr = server(conn_sock,lst,db_conn)
sr.recv_msgs()