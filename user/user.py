from socket import *
from db.db import db
from chatroom.chatroom import *
from db.db import *
import pickle
class User():

    def __init__(self,name:str,id_num:int,password:str,ip_addr:str,is_sys_admin:bool,sock:socket):
        self.joined_room = []
        self.admin_in = []
        self.name = name
        self.password = password
        self.ip_addr = ip_addr
        self.is_sys_admin = is_sys_admin
        self.sock = sock
        self.id_num = id_num
    
    @classmethod
    def from_ip(cls,ip_addr:str,sock:socket) -> 'User':
        return cls('tmp','tmp',ip_addr,False,sock)

    def join_room(self,chatroom_id:int,db_conn:db) -> None:
        self.joined_room.append(db_conn.get_chat(chatroom_id))

    

