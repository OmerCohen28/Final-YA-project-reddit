from socket import *
class User():

    def __init__(self,name:str,password:str,ip_addr:str,is_sys_admin:bool,socket:socket):
        self.joined_room = []
        self.admin_in = []
        self.name = name
        self.password = password
        self.ip_addr = ip_addr
        self.is_sys_admin = is_sys_admin
        self.socket = socket