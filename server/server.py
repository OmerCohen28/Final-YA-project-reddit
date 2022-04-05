from socket import *
from user.user import *
from db.db import *
from user.user import *
from socket import *
import select
import pickle

class server:
    curr_chat_ip =0 #since the server gives the chat id, i created a class variable
                    # to keep track of the current id between all instances
    curr_user_id=0 #same thing for users

    def __init__(self,conn_sock:socket,all_sockets:list[socket],sock_user_dict:dict[socket:User],user_sock_dict:dict[User:socket],db_conn:db):
        self.conn_sock = conn_sock
        self.all_sockets = all_sockets
        self.sock_user_dict = sock_user_dict
        self.user_sock_dict = user_sock_dict
        self.db_conn = db_conn


    '''
    This function is the main function that should be used to create new users, it updates the user id 
    variable and add the user to the database. If None is returned, it means there has been an eror
    '''
    def create_new_user(self,name:str,password:str,ip_addr:str,is_sys_admin:bool,sock:socket) ->User/None:
        user = User(name,self.curr_user_id,password,ip_addr,is_sys_admin,sock)
        if(self.add_user_to_db(user)):
            self.sock_user_dict[sock] = User
            self.user_sock_dict[User] = sock
            self.curr_user_ip+=1
            return user
        return None

    '''
    alternative function that recevies a list with all the data and creates the new user
    list content:  name(str), password(str),ip_addr(str), is_sys_admin(bool),sock(socket)
    '''
    def create_new_user_from_lst(self,info:list)->User/None:
        user = User(info[0],self.curr_user_id,info[1],info[2],info[3],info[4])
        if(self.add_user_to_db(user)):
            self.sock_user_dict[info[4]] = User
            self.user_sock_dict[User] = info[4]
            self.curr_user_id+=1
            return user
        return None

    
    '''
    this function group is devoted to interacting with the DB
    '''
    def add_user_to_db(self,user:User)->bool:
        return self.db_conn.insert_user(user)

    def get_user_by_id(self,id_num:int)-> User/None:
        user = self.db_conn.get_user(id_num)
        if user is User:
            return user
        return None
    
    def del_user_by_id(self,id_num:int) ->bool:
        return self.db_conn.delete_user(str(id_num))

    '''
    group of functions devoted to receving new connections, users and chatrooms and handling adding them
    to the DB and overall system
    '''

    #main receving function
    def recv_msgs(self):
        while True:
            read,write,eror = select.select(self.all_sockets,[],[])

            if read==self.conn_sock:
                client_sock = self.conn_sock.accept()
                self.all_sockets.append(client_sock)
            else:
                msg = read.recv(1054).decode()
                if(msg=='new user'):
                    self.get_new_user_data()

    '''
    expected input : name(str),password(str),ip_addr(str), is_sys_admin(bool))
    expected output: None
    '''
    def get_new_user_data(self,sock:socket) ->None:
        sock.send('waiting for data'.encode())
        msg = sock.recv(1054).decode()
        while msg!='done':
            user_info = [msg]
            sock.send('ok'.encode())
            msg = sock.recv(1054).decode()
        user_info.append(sock)
        user = self.create_new_user_from_lst(user_info)
        sock.send(pickle.loads(user))
        
        


                    

    