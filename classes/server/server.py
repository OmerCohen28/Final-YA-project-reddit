import datetime
from itertools import count
from socket import *
from classes.chatroom.chatroom import chatroom
from classes.user.user import User
from model import db
from select import select
import pickle
from os.path import exists
import time
import rake_nltk
import re

class server:
    curr_chat_id =0 #since the server gives the chat id, i created a class variable
                    # to keep track of the current id between all instances
    chat_name_to_id_dict = {} #dict to help convert chat_room names to id, used when getting
                              #a room by name
    def __init__(self,db_conn:db):
        self.conn_sock = socket(AF_INET,SOCK_STREAM)
        self.conn_sock.bind(("localhost",50000))
        self.conn_sock.listen(5)
        self.conn_sock.setsockopt(SOL_SOCKET,SO_REUSEADDR, True)
        self.all_sockets = [self.conn_sock]
        self.db_conn = db_conn
        self.current_user_chat_room_dict = {}
        self.current_user_socket_dict = {}
        self.users_time_dict = {}
        self.initialize_server_core_vars()
        self.rake_obj = rake_nltk.Rake('stop.txt')
        self.udp_sock = socket(AF_INET,SOCK_DGRAM)
        self.udp_sock.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
        self.udp_sock.bind(("",50501))

    '''
    core functions that the server uses
    '''
    def initialize_server_core_vars(self):
        self.curr_chat_id = self.db_conn.get_current_chat_room_id()
        if self.curr_chat_id is None:
            self.curr_chat_id = 0
            self.db_conn.set_current_chat_room_id(0)

        self.chat_name_to_id_dict = self.db_conn.get_current_chat_name_to_id_dict()
        if self.chat_name_to_id_dict is None:
            self.chat_name_to_id_dict = {}
            self.db_conn.set_current_chat_name_to_id_dict({})
    '''
    RAKE function group
    '''     
    def get_all_words_from_chats(self):
        id_text_dict = {}
        for id_num in range(self.curr_chat_id):
            text = ""
            chat_room = self.db_conn.get_chat(id_num)
            if isinstance(chat_room,str):
                continue
            for msg in chat_room.msgs:
                text+= f". {msg.msg}"
            id_text_dict[id_num] = text
        return id_text_dict

    def get_word_score_dict_for_chat_room(self,id_num) ->dict:
        id_text_dict = self.get_all_words_from_chats()
        text = id_text_dict[id_num]
        self.rake_obj.extract_keywords_from_text(text)
        word_score_dict = self.rake_obj.get_word_degrees()
        return word_score_dict


    def clac_the_score_of_a_word_in_chat(self,id_num:int,word:str)->int:
        id_text_dict = self.get_all_words_from_chats()
        text = id_text_dict[id_num]
        self.rake_obj.extract_keywords_from_text(text)
        word_score_dict = self.rake_obj.get_word_degrees()
        return word_score_dict[word]
    
    def make_room_score_dict(self,keyword:str):
        final_dict = {}
        for i in range(self.curr_chat_id):
            chat_room = self.db_conn.get_chat(i)
            if isinstance(chat_room,str):
                continue
            final_dict[chat_room] = self.clac_the_score_of_a_word_in_chat(i,keyword)
        return final_dict

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
            print('returned true man')
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

    def add_chatroom_to_db(self,chatroom:chatroom) ->bool:
        if not self.check_if_chatroom_name_exists(chatroom.name):
            id_num = chatroom.room_id
            self.chat_name_to_id_dict[chatroom.name] = id_num
            self.db_conn.set_current_chat_name_to_id_dict(self.chat_name_to_id_dict)
            return self.db_conn.insert_chat(id_num,chatroom)
        return False

    def check_if_chatroom_name_exists(self,name:str) ->bool:
        try:
            id_num = self.chat_name_to_id_dict[name]
        except:
            return False
        tmp = self.db_conn.get_chat(id_num)

        try:
            x = tmp.msgs
            return True
        except:
            return False
    
    def get_name_to_id_chat_room_name_dict(self)->dict:
        result = {}
        for id_num in range(self.curr_chat_id):
            if isinstance(chat_room,str):
                continue
            chat_room = self.db_conn.get_chat(id_num)
            result[chat_room.name] = id_num
        return result
    
    def check_if_rooms_are_expired_and_replace(self):
        for i in range(self.curr_chat_id):
            chat_room = self.db_conn.get_chat(i)
            if isinstance(chat_room,str):
                continue
            if time.time() - chat_room.time_untill_expire <0.1:
                self.db_conn.insert_chat(i,"expired")

    '''
    group of functions devoted to receving new connections, users and chatrooms and handling adding them
    to the DB and overall system
    '''

    # "main" function
    def recv_msgs(self):
        while True:
            lst = self.all_sockets
            read,write,eror = select(lst,[],[],0)
            for sockobj in read:
                print("again")
                print(f"dict: {self.current_user_chat_room_dict}")
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
                    print(msg)
                    if(msg=='new user'):
                        self.get_new_user_data(sockobj)
                    if(msg=="log in"):
                        self.check_log_in(sockobj)
                    if(msg=="need chat id"):
                        sockobj.send(pickle.dumps(self.curr_chat_id))
                        self.curr_chat_id+=1
                        self.db_conn.set_current_chat_room_id(self.curr_chat_id)
                    if(msg=="is exist"):
                        self.check_new_chatroom_name(sockobj)
                    if(msg=="new room"):
                        self.get_new_room_and_add_to_db(sockobj)
                    if(msg[0:14]=="get room by id"):
                        self.return_room_by_id(sockobj,msg)
                    if(msg=="room name dict"):
                        self.get_room_by_name_and_call_id_func(sockobj,msg)
                    if(msg=="new msg"):
                        self.get_new_message_and_add_to_db(sockobj)
                    if(msg=="leaving"):
                        sockobj.send(pickle.dumps("who?"))
                        user_leaving = pickle.loads(sockobj.recv(1054))
                        try:
                            del self.current_user_chat_room_dict[user_leaving]
                            del self.current_user_socket_dict[user_leaving]
                            del self.users_time_dict[user_leaving]
                        except KeyError:
                            pass
                    if(msg=="search"):
                        self.return_to_client_room_score_dict(sockobj)
                    if(msg[0:15] == "change password"):
                        self.chage_password(sockobj,msg)
                    if(msg[0:8]=="add user"):
                        self.add_user_to_chat_room(sockobj,msg)
                    if(msg=="chat id"):
                        sockobj.send(pickle.dumps(self.curr_chat_id))
                    if(msg=="get all users time dict"):
                        self.return_user_time_dict_to_admin(sockobj)
                    if(msg=="get all users chatroom dict"):
                        self.return_user_chat_room_dict_to_admin(sockobj)


    '''
    function group to deal with requests from clients and respond
    '''

    '''
    expected input : name(str),password(str), is_sys_admin(bool))
    expected output: None
    '''
    def get_new_user_data(self,sock:socket) ->None:
        sock.send(pickle.dumps('waiting for data'))
        user_info = pickle.loads(sock.recv(1054))
        sock.send(pickle.dumps("ok"))
        is_ok = self.create_new_user_from_lst(user_info)
        print(f"server said {is_ok}")
        sock.send(pickle.dumps(is_ok))
    
    def check_log_in(self,sock:socket) -> None:
        sock.send(pickle.dumps("waiting for data"))
        user_info_lst = pickle.loads(sock.recv(1054))
        name = user_info_lst[0]
        password = user_info_lst[1]
        sock.send(pickle.dumps("ok"))
        end = pickle.loads(sock.recv(1054))
        if(end=="done"):
            check = self.db_conn.get_user(name)
            if(check=="key didn't have a value"):
                sock.send(pickle.dumps(("no username","")))
                return
            if(password == check.password):
                sock.send(pickle.dumps(('ok',check)))
                self.current_user_socket_dict[name] = sock
                self.users_time_dict[name]=datetime.datetime.now()
                return
            sock.send(pickle.dumps(("password is inccorect","")))
    
    def chage_password(self,sock:socket,info:str):
        name_pattern = re.compile(r"name:<(.+?)>")
        new_pass_pattern = re.compile(r"password:<(.+?)>")
        name = re.findall(string=info,pattern=name_pattern)[0]
        new_pass = re.findall(string=info,pattern=new_pass_pattern)[0]
        user = self.db_conn.get_user(name)
        user.password = new_pass
        result = self.db_conn.update_user(user)
        sock.send(pickle.dumps(result))

    def add_user_to_chat_room(self,sock:socket,info:str):
        user_name_pattern =  re.compile(r"name:<(.+?)>")
        room_id_pattern = re.compile(r"chat:<(.+?)>")
        user_name = re.findall(string=info,pattern=user_name_pattern)[0]
        room_id = re.findall(string=info,pattern=room_id_pattern)[0]

        user = self.db_conn.get_user(user_name)
        chat_room = self.db_conn.get_chat(room_id)
        if isinstance(chat_room,str):
            sock.send(pickle.dumps("no chat room"))
        if chat_room.add_user(user):
            sock.send(pickle.dumps(True))
            print("sent true")
            self.db_conn.insert_chat(chat_room.room_id,chat_room)
            self.notify_all_members_of_chatroom_for_new_msg(chat_room)
            return
        print("sent false")
        sock.send(pickle.dumps(False))



    def check_new_chatroom_name(self,sock:socket):
        sock.send(pickle.dumps("send name"))
        name = pickle.loads(sock.recv(1054))
        sock.send(pickle.dumps(self.check_if_chatroom_name_exists(name)))

    def get_new_room_and_add_to_db(self,sock:socket):
        sock.send(pickle.dumps("ok"))
        new_room = pickle.loads(sock.recv(1054))
        sock.send(pickle.dumps(self.add_chatroom_to_db(new_room)))
    
    def return_room_by_id(self,sock:socket,info):
        id_pattern = re.compile(r"id:<(\d+)>")
        name_pattern = re.compile(r"name:<(.+?)>")
        id_num = re.findall(pattern=id_pattern,string=info)[0]
        name = re.findall(pattern=name_pattern,string = info)[0]
        print(id_num)
        print(name)
        chat_room = self.db_conn.get_chat(id_num)
        if name!="no":
            self.current_user_chat_room_dict[name] = id_num
        try:
            chat_room.current_members = self.get_how_many_members_are_online_to_a_room(id_num)
        except AttributeError:
            sock.send(pickle.dumps("no chatroom"))
            time.sleep(0.5)
            sock.send("stop".encode())
            print('no chatroom')
            return
        sock.send(pickle.dumps(chat_room))
        print('sent chatroom')
        print(chat_room)
        time.sleep(0.5)
        sock.send("stop".encode())
        msg = pickle.loads(sock.recv(1054))
        if msg == "no need":
            print("yeh")
            return
        sock.send(pickle.dumps("need what?"))
        need = pickle.loads(sock.recv(1054))
        print(need)
        for img_name in need:
            self.send_picture(sock,img_name)
    
    def get_how_many_members_are_online_to_a_room(self,id_num):
        count=0
        for key in self.current_user_chat_room_dict:
            if self.current_user_chat_room_dict[key] == id_num:
                count+=1
        return count

    def get_picture_and_save(self,sock:socket,img_name:str):
            img = b""
            while True:
                packet = sock.recv(1054)
                if packet == "stop".encode():
                    break
                img+=packet
            with open(f"server_pics\\{img_name}",'wb') as new_img:
                new_img.write(img)
    
    def send_picture(self,sock,img_name):
        with open(f"server_pics\\{img_name}",'rb') as img:
            sock.send(img.read())
            time.sleep(0.5)
            sock.send("stop".encode())     

    def get_new_message_and_add_to_db(self,sock:socket):
        print('sup')
        sock.send(pickle.dumps("send msg"))
        print('supsup?')
        data = sock.recv(1054)
        while True:
            packet = sock.recv(1054)
            if packet == "stop".encode():
                break
            data+=packet
        new_msg = pickle.loads(data)
        sock.send(pickle.dumps("ok"))
        if new_msg.img_name != "":   
            if exists(f"server_pics\\{new_msg.img_name}"):
                extension_name = new_msg.img_name[new_msg.img_name.find(".")+1:]
                new_msg.img_name = new_msg.img_name[:new_msg.img_name.find(".")]+f'1.{extension_name}'
            self.get_picture_and_save(sock,new_msg.img_name)
        print(new_msg.img_name)
        chat_room = new_msg.sent_in
        chat_room.msgs.append(new_msg)
        self.db_conn.insert_chat(chat_room.room_id,chat_room)
        self.notify_all_members_of_chatroom_for_new_msg(chat_room)

    def notify_all_members_of_chatroom_for_new_msg(self,chat_room):
        print('in refresh function')
        for name in self.current_user_chat_room_dict:
            if self.current_user_chat_room_dict[name] == str(chat_room.room_id):
                sock = self.current_user_socket_dict[name]
                ip_addr,port = sock.getsockname()
                print('sent refresh msg')
                self.udp_sock.sendto(pickle.dumps("need refresh"),(ip_addr,50100))
               
                
    
    def return_to_client_room_score_dict(self,sockobj:socket):
        sockobj.send(pickle.dumps("what is the word"))
        print('sent')
        keyword = pickle.loads(sockobj.recv(1054))
        print('got it')
        dict_to_send = self.make_room_score_dict(keyword)
        print(f"dict {dict_to_send}")
        sockobj.send(pickle.dumps(dict_to_send))
        time.sleep(0.5)
        sockobj.send("stop".encode())

    def get_room_by_name_and_call_id_func(self,sockobj:socket,info):
        id_name_dict = self.get_name_to_id_chat_room_name_dict()
        sockobj.send(pickle.dumps(id_name_dict))
        time.sleep(0.5)
        sockobj.send("stop".encode())

    def return_user_time_dict_to_admin(self,sock:socket):
        sock.send(pickle.dumps(self.users_time_dict))
        time.sleep(0.5)
        sock.send("stop".encode())
    
    def return_user_chat_room_dict_to_admin(self,sock:socket):
        new_dict = {}

        id_to_name_dict = {v: k for k, v in self.chat_name_to_id_dict.items()}
        print("id to name:",id_to_name_dict)
        print("user chat room:",self.current_user_chat_room_dict)
        print("chat name to id",self.chat_name_to_id_dict)
        for key in self.current_user_chat_room_dict:
            print(key)
            try:
                new_dict[key] = id_to_name_dict[self.current_user_chat_room_dict[key]]
                print("done")
            except KeyError:
                pass
        print(new_dict)
        sock.send(pickle.dumps(new_dict))
        time.sleep(0.5)
        sock.send("stop".encode())

        
        


                    

    