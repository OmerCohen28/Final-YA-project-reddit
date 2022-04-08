import sys
from socket import *
import pickle
from classes.user.user import User
class user_controller:
    def __init__(self):
        self.sock = socket(AF_INET,SOCK_STREAM)
        port = user_controller.get_open_port()
        self.sock.setsockopt(SOL_SOCKET,SO_REUSEADDR, True)
        self.sock.bind(("localhost",port))
        print(port)
        self.sock.connect(("localhost",50000))

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

