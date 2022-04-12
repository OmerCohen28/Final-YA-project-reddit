from ast import Str
import sys
from socket import *
import pickle
from classes.user.user import User
from classes.chatroom.chatroom import chatroom
from classes.message.message import message
import random
class user_controller:
    def __init__(self):
        while True:
            try:
                self.sock = socket(AF_INET,SOCK_STREAM)
                port = user_controller.get_port()
                self.sock.setsockopt(SOL_SOCKET,SO_REUSEADDR, True)
                self.sock.bind(("localhost",port))
                print(port)
                self.sock.connect(("localhost",50000))
                break
            except:
                pass

    def close_sock(self):
        self.sock.close()


    def sign_up(self,name,password,is_sys_admin):
        #if there is a problem with the IP recognition it lies here
        msgs = ['new user',name,password,is_sys_admin]
        for msg in msgs:
            self.sock.send(pickle.dumps(msg))
            new_msg = pickle.loads(self.sock.recv(1054))
        self.sock.send(pickle.dumps('done'))
        is_ok = pickle.loads(self.sock.recv(1054))
        return is_ok
    
    def log_in(self,name:str,password:str) ->bool:
        msgs = ['log in',name,password]
        for msg in msgs:
            self.sock.send(pickle.dumps(msg))
            new_msg = pickle.loads(self.sock.recv(1054))
        self.sock.send(pickle.dumps('done'))
        msg = pickle.loads(self.sock.recv(1054))
        return msg

    def get_msgs_for_main_menu(self):
        return msgs

    def create_new_room_with_server(self,creator:User,name:str,topic:str) -> bool:
        print("starting procces")
        id_num = self.get_new_room_id_from_server()
        new_chat = chatroom(creator,name,[topic],id_num,[])
        if not self.check_if_room_name_exists(name):
            self.sock.send(pickle.dumps("new room"))
            self.sock.recv(1054)
            self.sock.send(pickle.dumps(new_chat))
            return pickle.loads(self.sock.recv(1054))
        return False

    def get_new_room_id_from_server(self):
        print("getting new id")
        self.sock.send(pickle.dumps("need chat id"))
        new_id = int(pickle.loads(self.sock.recv(1054)))
        print(new_id)
        return new_id

    def check_if_room_name_exists(self,name:str) ->bool:
        print("checking if exists")
        self.sock.send(pickle.dumps("is exist"))
        tmp = self.sock.recv(1054)
        print(tmp)
        self.sock.send(pickle.dumps(name))
        print('sent')
        result = pickle.loads(self.sock.recv(1054))
        print(result)
        return result

    @staticmethod
    def get_open_port():
        start_port = 50002
        for i in range(start_port,start_port+3000):
            sock = socket(AF_INET,SOCK_DGRAM)
            try:
                sock.bind(("",i))
                return i
            except:
                pass
    
    @staticmethod
    def get_port():
        starting_port = user_controller.get_open_port()
        rand_num = random.randint(10,30)
        if( starting_port+rand_num < 50500): return starting_port + rand_num
        return starting_port-rand_num

use = User("ayal","123",False)

chat = chatroom(use,"Omer's WonderLand",[],1,[])                    

msg1 = message("omer","wow this works!!",chat,"user.png","Please work")
msg2 = message("itai","Pleeeeeeeeeeeeeeeeeeeeeeeeeaaaaaaaaaaaaaaaaaaasssssssssssssssseeeeeeeeeeeeeeeeeeeee",chat,"cat.jpg","holy fuck please")
msg3 = message("elad","testingeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee",chat,"logo.png","testing")
msg4 = message("benny","Will This Appear eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee??",chat,"no","Will you see meeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee?")
msgs = [msg1,msg2,msg4,msg3]
msg3.add_comment(msg1)
msg3.add_comment(msg4)
msg4.add_comment(msg1)
msg4.add_comment(msg4)