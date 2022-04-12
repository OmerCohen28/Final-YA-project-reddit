import select
from socket import *
from classes.server.server import *
from model import *




db_conn = db()
sr = server(db_conn)
sr.recv_msgs()
