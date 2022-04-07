import sys
from socket import *
import pickle
from user.user import User
class user_controller:
    def __init__(self):
        self.sock = socket(AF_INET,SOCK_STREAM)
        port = user_controller.get_open_port()
        self.sock.bind(("127.0.0.1",port))
        print(port)
        self.sock.connect(("127.0.0.1",50000))

    def sign_up(self,name,password,is_sys_admin):
        #if there is a problem with the IP recognition it lies here
        ip_addr = gethostbyname_ex(gethostname())[2][0] 
        msgs = ['new user',name,password,ip_addr,is_sys_admin]
        for msg in msgs:
            print(msg)
            self.sock.send(pickle.dumps(msg))
            new_msg = pickle.loads(self.sock.recv(1054))
        self.sock.send(pickle.dumps('done'))
        new_user = pickle.loads(self.sock.recv(1054))
        return new_user

    @staticmethod
    def get_open_port():
        start_port = 50001
        for i in range(start_port,start_port+3000):
            sock = socket(AF_INET,SOCK_DGRAM)
            try:
                sock.bind(("",i))
                return i
            except:
                pass

