import sys
from socket import *
import pickle
from classes.user.user import User
from classes.chatroom.chatroom import chatroom
from classes.message.message import message
import random
import time
from os.path import exists
from select import select
class user_controller:
    def __init__(self):
        while True:
            try:
                self.sock = socket(AF_INET,SOCK_STREAM)
                port = user_controller.get_port()
                self.sock.setsockopt(SOL_SOCKET,SO_REUSEADDR, True)
                self.sock.bind(("localhost",port))
                print(port)
                self.sock.connect(("localhost",50000))
                break
            except:
                pass
        self.refresh = False
        self.in_process = False

    def close_connection(self,name):
        self.in_process = True
        self.sock.send(pickle.dumps("leaving"))
        who_leaves = self.get_current_waiting_msg()
        print(who_leaves)
        self.sock.send(pickle.dumps(name))
        self.sock.close()

    def get_current_waiting_msg(self):
        try:
            read,write,eror = select([self.sock],[],[],1)
            msg = pickle.loads(read[0].recv(1054))
        except:
            try:
                return msg
            except:
                return None
        if msg != "need refresh":
            return msg 
        self.refresh = True

    def get_large_data(self):
        self.in_process = True
        data = b""
        print('getting large data')
        while True:
            packet = self.sock.recv(1054)
            if packet == "stop".encode():
                break
            data+=packet
        msg = pickle.loads(data)
        self.in_process = False
        return msg


    def sign_up(self,name,password,is_sys_admin):
        self.in_process = True
        #if there is a problem with the IP recognition it lies here
        msgs = ['new user',name,password,is_sys_admin]
        for msg in msgs:
            self.sock.send(pickle.dumps(msg))
            new_msg = self.get_current_waiting_msg()
        self.sock.send(pickle.dumps('done'))
        is_ok = self.get_current_waiting_msg()
        self.in_process = False
        return is_ok
    
    def log_in(self,name:str,password:str) ->bool:
        self.in_process = True
        msgs = ['log in',name,password]
        for msg in msgs:
            print('sending')
            self.sock.send(pickle.dumps(msg))
            print('sent')
            print(msg)
            new_msg = self.get_current_waiting_msg()
        self.sock.send(pickle.dumps('done'))
        msg = self.get_current_waiting_msg()
        self.in_process = False
        return msg

    def get_msgs_for_main_menu(self):
        self.in_process = True
        self.in_process = False
        return msgs

    def create_new_room_with_server(self,creator:User,name:str,topics,banned_words) -> bool:
        print("starting procces")
        id_num = self.get_new_room_id_from_server()
        new_chat = chatroom(creator,name,topics,id_num,banned_words)
        if not self.check_if_room_name_exists(name):
            self.sock.send(pickle.dumps("new room"))
            self.get_current_waiting_msg()
            self.sock.send(pickle.dumps(new_chat))
            self.in_process = False
            return self.get_current_waiting_msg()
        self.in_process = False
        return False

    def get_new_room_id_from_server(self):
        self.in_process = True
        print("getting new id")
        self.sock.send(pickle.dumps("need chat id"))
        new_id = int(self.get_current_waiting_msg())
        print(new_id)
        self.in_process = False
        return new_id

    def check_if_room_name_exists(self,name:str) ->bool:
        self.in_process = True
        print("checking if exists")
        self.sock.send(pickle.dumps("is exist"))
        tmp = self.get_current_waiting_msg()
        print(tmp)
        self.sock.send(pickle.dumps(name))
        print('sent')
        result = self.get_current_waiting_msg()
        print(result)
        self.in_process = False
        return result
    
    def get_room_by_id(self,id_num:int,name:str) ->chatroom:
        self.in_process = True
        self.sock.send(pickle.dumps("get room by id"))
        msg = self.get_current_waiting_msg()
        print(msg)
        self.sock.send(pickle.dumps(id_num))
        print('sent id')
        ok_msg = self.get_current_waiting_msg()
        print(ok_msg)
        self.sock.send(pickle.dumps(name))
        print('sent name')
        ok_msg = self.get_current_waiting_msg()
        print(ok_msg)
        chat_room = self.get_large_data()
        if not isinstance(chat_room,chatroom):
            print(chat_room)
            print(type(chat_room))
            self.in_process = False
            return False
        need_imgs_names = []
        for msg in chat_room.msgs:
            if not exists(f"pictures\\{msg.img_name}"):
                need_imgs_names.append(msg.img_name)
        if len(need_imgs_names) > 0:
            self.sock.send(pickle.dumps("need"))
            print('sent need')
            need_what = self.get_current_waiting_msg()
            print(need_what)
            self.sock.send(pickle.dumps(need_imgs_names))

            for img_name in need_imgs_names:
                self.get_picture_and_save(img_name)
        else:
            self.sock.send(pickle.dumps("no need"))
            print('sent no need')

        self.in_process = False
        return chat_room
    
    def create_message_and_sent_to_server(self,name:str,msg:str,chat_room:chatroom,img_path_and_name:str,title:str):
        self.in_process = True
        if img_path_and_name != "":
            img_name = img_path_and_name[img_path_and_name.rfind("/")+1:]
        else:
            img_name = ""
        new_msg = message(name,msg,chat_room,img_name,title)
        self.sock.send(pickle.dumps("new msg"))
        send_msg = self.get_current_waiting_msg()
        print(send_msg)
        self.sock.send(pickle.dumps(new_msg))
        time.sleep(0.5)
        self.sock.send("stop".encode())
        ok_msg = self.get_current_waiting_msg()
        print(ok_msg)
        if img_name != "":
            with open(img_path_and_name,'rb') as img:
                self.sock.send(img.read())
                time.sleep(0.5)
                self.sock.send("stop".encode())
        self.in_process = False

                
    def get_picture_and_save(self,img_name:str):
        self.in_process = True
        img = b""
        while True:
            packet = self.sock.recv(1054)
            if packet == "stop".encode():
                break
            img+=packet
        with open(f"pictures\\{img_name}",'wb') as new_img:
            new_img.write(img)
        self.in_process = False

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
    
    @staticmethod
    def get_port():
        starting_port = user_controller.get_open_port()
        rand_num = random.randint(10,30)
        if( starting_port+rand_num < 50500): return starting_port + rand_num
        return starting_port-rand_num

use = User("ayal","123",False)
chat = chatroom(use,"Omer's WonderLand",[],1,[])                    
chat2 = chatroom(use,"Omer's WonderLand 2nd edition",[],2,[])
msg1 = message("omer","wow this works!!",chat,"user.png","Please work")
msg2 = message("itai","Pleeeeeeeeeeeeeeeeeeeeeeeeeaaaaaaaaaaaaaaaaaaasssssssssssssssseeeeeeeeeeeeeeeeeeeee",chat,"cat.jpg","holy fuck please")
msg3 = message("elad","testingeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee",chat,"logo.png","testing")
msg4 = message("benny","Will This Appear eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee??",chat,"no","Will you see meeeeeeeeeeeeeeeee?")
msg5 = message("omer2","Hello",chat2,"reddit-logo.png","Wow hello there")
msgs = [msg1,msg2,msg4,msg3,msg5]
msg3.add_comment(msg1)
msg3.add_comment(msg4)
msg4.add_comment(msg1)
msg4.add_comment(msg4)
chat2.add_msg(msg5)
chat.msgs = [msg1,msg2,msg3,msg4]