from socket import *
from classes.user.user import User
from classes.db.db import db
from select import select
import pickle

class server:
    curr_chat_ip =0 #since the server gives the chat id, i created a class variable
                    # to keep track of the current id between all instances
    curr_user_id=0 #same thing for users

    def __init__(self,db_conn:db):
        self.conn_sock = socket(AF_INET,SOCK_STREAM)
        self.conn_sock.bind(("localhost",50000))
        self.conn_sock.listen(5)
        self.all_sockets = [self.conn_sock]
        self.db_conn = db_conn


    '''
    This function is the main function that should be used to create new users, it updates the user id 
    variable and add the user to the database. If None is returned, it means there has been an eror
    '''
    def create_new_user(self,name:str,password:str,ip_addr:str,is_sys_admin:bool) ->User:
        user = User(name,self.curr_user_id,password,ip_addr,is_sys_admin)
        if(self.add_user_to_db(user)):
            self.curr_user_ip+=1
            return user
        return None

    '''
    alternative function that recevies a list with all the data and creates the new user
    list content:  name(str), password(str),ip_addr(str), is_sys_admin(bool),sock(socket)
    '''
    def create_new_user_from_lst(self,info:list)->User:
        user = User(info[0],self.curr_user_id,info[1],info[2],info[3])
        if(self.add_user_to_db(user)):
            self.curr_user_id+=1
            return user
        return None

    
    '''
    this function group is devoted to interacting with the DB
    '''
    def add_user_to_db(self,user:User)->bool:
        return self.db_conn.insert_user(user)

    def get_user_by_id(self,id_num:int)-> User:
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
            lst = self.all_sockets
            read,write,eror = select(lst,[],[],0)
            for sockobj in read:
                if sockobj==self.conn_sock:
                    print("hi")
                    client_sock,address = self.conn_sock.accept()
                    self.all_sockets.append(client_sock)
                else:
                    msg = pickle.loads(sockobj.recv(1054))
                    print('message')
                    if(msg=='new user'):
                        self.get_new_user_data(sockobj)

    '''
    expected input : name(str),password(str),ip_addr(str), is_sys_admin(bool))
    expected output: None
    '''
    def get_new_user_data(self,sock:socket) ->None:
        print('here')
        sock.send(pickle.dumps('waiting for data'))
        msg = pickle.loads(sock.recv(1054))
        user_info = []
        while msg!='done':
            user_info.append(msg)
            sock.send(pickle.dumps('ok'))
            msg = pickle.loads(sock.recv(1054))
        print(user_info)
        user = self.create_new_user_from_lst(user_info)
        print(user)
        sock.send(pickle.dumps(user))
        
        


                    

    