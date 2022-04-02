from socket import *
from user.user import *
from db.db import *
from user.user import *
from socket import *
class server:
    curr_chat_ip =0 #since the server gives the chat id, i created a class variable
                    # to keep track of the current id between all instances
    curr_user_ip=0
    def __init__(self,conn_sock:socket,all_sockets:list[socket],sock_user_dict:dict[socket:User],db_conn:db) -> None:
        self.conn_sock = conn_sock
        self.all_sockets = all_sockets
        self.sock_user_dict = sock_user_dict
        self.db_conn = db_conn


    '''
    This function is the main function that should be used to create new users, it updates the user id 
    variable and add the user to the database. If None is returned, it means there has been an eror
    '''
    def create_new_user(self,name:str,id_num:int,password:str,ip_addr:str,is_sys_admin:bool,sock:socket) ->User/None:
        user = User(name,id_num,password,ip_addr,is_sys_admin,sock)
        if(self.add_user_to_db(user)):
            return user
        return None

    def add_user_to_db(self,user:User)->bool:
        return self.db_conn.insert_user(user)

    def get_user_by_id(self,id_num:int)-> User/None:
        user = self.db_conn.get_user(id_num)
        if user is User:
            return user
        return None
    
    def del_user_by_id(self,id_num:int) ->bool:
        return self.db_conn.delete_user(str(id_num))

    