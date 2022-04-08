import select
from socket import *
from classes.server.server import *
from classes.db.db import *




db_conn = db()
sr = server(db_conn)
sr.recv_msgs()
