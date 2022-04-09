from socket import *
from classes.user.user import User
from classes.db.db import db
from select import select
import pickle

class server:
    curr_chat_ip =0 #since the server gives the chat id, i created a class variable
                    # to keep track of the current id between all instances
    chat_name_to_id_dict = {}
    def __init__(self,db_conn:db):
        self.conn_sock = socket(AF_INET,SOCK_STREAM)
        self.conn_sock.bind(("localhost",50000))
        self.conn_sock.listen(5)
        self.conn_sock.setsockopt(SOL_SOCKET,SO_REUSEADDR, True)
        self.all_sockets = [self.conn_sock]
        self.db_conn = db_conn



    '''
    This function is the main function that should be used to create new users, it updates the user id 
    variable and add the user to the database. If None is returned, it means there has been an eror
    '''
    def create_new_user(self,name:str,password:str,is_sys_admin:bool) ->bool:
        user = User(name,password,is_sys_admin)
        if(self.add_user_to_db(user)):
            return True
        return False

    '''
    alternative function that recevies a list with all the data and creates the new user
    list content:  name(str), password(str), is_sys_admin(bool)
    '''
    def create_new_user_from_lst(self,info:list)->bool:
        user = User(info[0],info[1],info[2])
        if(self.add_user_to_db(user)):
            return True
        return False

    
    '''
    this function group is devoted to interacting with the DB
    '''
    def add_user_to_db(self,user:User)->bool:
        return self.db_conn.insert_user(user)

    def get_user_by_name(self,id_num:int)-> User:
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
                print("again")
                if sockobj==self.conn_sock:
                    client_sock,address = self.conn_sock.accept()
                    self.all_sockets.append(client_sock)
                else:
                    try:
                        msg = sockobj.recv(1054)
                    except ConnectionResetError:
                        del lst[lst.index(sockobj)]
                        sockobj.close()
                        continue    
                    if not msg:
                        del lst[lst.index(sockobj)]
                        sockobj.close()
                        continue                   
                    msg = pickle.loads(msg)
                    if(msg=='new user'):
                        self.get_new_user_data(sockobj)
                    if(msg=="log in"):
                        self.check_log_in(sockobj)
                        print('done')

    '''
    expected input : name(str),password(str), is_sys_admin(bool))
    expected output: None
    '''
    def get_new_user_data(self,sock:socket) ->None:
        sock.send(pickle.dumps('waiting for data'))
        msg = pickle.loads(sock.recv(1054))
        user_info = []
        while msg!='done':
            user_info.append(msg)
            sock.send(pickle.dumps('ok'))
            msg = pickle.loads(sock.recv(1054))
        is_ok = self.create_new_user_from_lst(user_info)
        sock.send(pickle.dumps(is_ok))
    
    def check_log_in(self,sock:socket) -> None:
        print('in')
        name = ""
        password = ""
        sock.send(pickle.dumps("waiting for data"))
        name = pickle.loads(sock.recv(1054))
        sock.send(pickle.dumps('ok'))
        password = pickle.loads(sock.recv(1054))
        sock.send(pickle.dumps('ok'))
        end = pickle.loads(sock.recv(1054))
        if(end=="done"):
            check = self.db_conn.get_user(name)
            if(check=="key didn't have a value"):
                sock.send(pickle.dumps(("no username","")))
                return
            if(password == check.password):
                sock.send(pickle.dumps(('ok',check)))
            sock.send(pickle.dumps(("password is inccorect","")))

        
        
        


                    

    