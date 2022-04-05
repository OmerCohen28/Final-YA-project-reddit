import select
from socket import *
from server.server import *
from db.db import *


db_conn = db()
conn_sock = socket(AF_INET,SOCK_STREAM)
conn_sock.bind(("",50000))
conn_sock.listen(5)
server = server(conn_sock,[conn_sock],{},db_conn)
server.recv_msgs()