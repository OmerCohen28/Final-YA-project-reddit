from socket import *
import pickle
class User():

    def __init__(self,name:str,id_num:int,password:str,ip_addr:str,is_sys_admin:bool):
        self.joined_room = []
        self.admin_in = []
        self.name = name
        self.password = password
        self.ip_addr = ip_addr
        self.is_sys_admin = is_sys_admin
        self.id_num = id_num
    
    def __str__(self):
        return f"name: {self.name}, id: {self.id_num}, ip: {self.ip_addr}"
    
    @classmethod
    def from_ip(cls,ip_addr:str,sock:socket) -> 'User':
        return cls('tmp','tmp',ip_addr,False,sock)


    

