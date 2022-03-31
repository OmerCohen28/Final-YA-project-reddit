from socket import *
from user.user import *
from db.db import *
from user.user import *

class server:
    curr_chat_ip =0 #since the server gives the chat id, i created a class variable
                    # to keep track of the current id between all instances
    def __init__(self,conn_sock:socket,all_sockets:list[socket],sock_user_dict:dict[socket:User],db_conn:db) -> None:
        self.conn_sock = conn_sock
        self.all_sockets = all_sockets
        self.sock_user_dict = sock_user_dict
        self.db_conn = db_conn