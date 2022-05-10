from socket import *
import pickle
class User():

    def __init__(self,name:str,password:str,is_sys_admin:bool):
        self.joined_room = []
        self.admin_in = []
        self.name = name
        self.password = password
        self.is_sys_admin = is_sys_admin
    
    def __str__(self):
        return f"name: {self.name}, password: {self.password}"
    


    

