from socket import *
import ssl
import warnings
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
        self.ip_addr = "10.100.102.3"
        warnings.filterwarnings("ignore",category=DeprecationWarning)
        #self.sock = ssl.wrap_socket(socket(AF_INET,SOCK_STREAM),server_side=False)
        self.sock = socket(AF_INET,SOCK_STREAM)
        self.sock.setsockopt(SOL_SOCKET,SO_REUSEADDR, True)
        self.sock.bind((self.ip_addr,0))
        self.sock.connect((self.ip_addr,50000))

        self.udp_sock = socket(AF_INET,SOCK_DGRAM)
        self.udp_sock.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
        self.udp_sock.bind((self.ip_addr,0))
        self.udp_porrt = self.udp_sock.getsockname()[1]

        self.refresh = False #alarms if refresh is needed
        self.banned = False #alarms the client if it has been banned
        self.kicked = False #alarms the client if it has been kicked
        self.in_process = False #alarms if any other function is waiting for a message before the ui checks if it needs a refresh
        self.large_data = False #alarms if there is a process of receving large data

    def close_connection(self,name):
        self.in_process = True
        self.sock.send(pickle.dumps("leaving"))
        print('from close connection')
        who_leaves = self.get_current_waiting_msg()
        self.sock.send(pickle.dumps(name))
        self.sock.close()
    

    def get_refresh_notification(self):
        read,write,eror = select([self.udp_sock],[],[],1)
        if len(read)==0:        
            return
        data,adress = self.udp_sock.recvfrom(1054)
        data = pickle.loads(data)
        print(f"data in refresh is {data}")
        if data == "need refresh":
            self.refresh = True
        if data == "banned":
            self.banned = True
        if data=="kicked":
            print("was told to get out")
            self.kicked = True

    def get_current_waiting_msg(self):
        print('taking data')
        if not self.large_data:
            try:
                read,write,eror = select([self.sock],[],[],4)
                msg = pickle.loads(read[0].recv(1054))
                print('got it')
                print(msg)
            except:
                try:
                    return msg
                except Exception as e:
                    print(e)
                    return None
            if msg != "need refresh":
                return msg 
            self.refresh = True

    def get_large_data(self):
        self.large_data = True
        data = b""
        print('getting large data')
        while True:
            print('loop')
            packet = self.sock.recv(1054)
            try:
                print(packet.decode())
            except:
                pass
            if packet == "stop".encode():
                break
            data+=packet
        msg = pickle.loads(data)
        self.large_data = False
        return msg


    def sign_up(self,name,password,is_sys_admin):
        self.in_process = True
        msgs = ['new user',[name,password,is_sys_admin]]
        for msg in msgs:
            self.sock.send(pickle.dumps(msg))
            print(msg)
            print('from sign up')
            new_msg = self.get_current_waiting_msg()
        print('from sign up')
        is_ok = self.get_current_waiting_msg()
        print(f"i am returning to ui: {is_ok}")
        self.in_process = False
        return is_ok
    
    def log_in(self,name:str,password:str) ->bool:
        self.in_process = True
        msgs = ['log in',[name,password]]
        for msg in msgs:
            print(msg)
            self.sock.send(pickle.dumps(msg))
            print('from log in')
            new_msg = self.get_current_waiting_msg()
            print(new_msg)
        self.sock.send(pickle.dumps('done'))
        print('from log in')
        msg = self.get_large_data()
        print("msg",msg)
        self.sock.send(pickle.dumps(self.udp_porrt)) #sending the current UDP port the client will be waiting for msgs on
        msg_waiting = self.get_current_waiting_msg()
        self.in_process = False
        return msg,msg_waiting
    
    def change_password(self,user:User,new_pass:str):
        self.sock.send(pickle.dumps(f"change password password:<{new_pass}> name:<{user.name}>"))
        result = self.get_current_waiting_msg()
        return result

    def get_msgs_for_main_menu(self):
        self.in_process = True
        self.in_process = False
        return msgs

    def join_room(self,user:User,chat_room:chatroom):
        self.sock.send(pickle.dumps(f"add user name:<{user.name}> to chat:<{chat_room.room_id}>"))
        result = self.get_current_waiting_msg()
        return result

    def create_new_room_with_server(self,creator:User,name:str,topics,banned_words) -> bool:
        self.in_process = True
        id_num = self.get_new_room_id_from_server()
        new_chat = chatroom(creator,name,topics,id_num,banned_words)
        if not self.check_if_room_name_exists(name):
            self.in_process = True
            self.sock.send(pickle.dumps("new room"))
            print('from create new room')
            self.get_current_waiting_msg()
            self.sock.send(pickle.dumps(new_chat))
            time.sleep(0.5)
            self.sock.send("stop".encode())
            self.in_process = False
            print('from create new room')
            return self.get_current_waiting_msg()
        self.in_process = False
        return False

    def get_new_room_id_from_server(self):
        self.sock.send(pickle.dumps("need chat id"))
        print('from get new room by id')
        new_id = int(self.get_current_waiting_msg())
        return new_id

    def check_if_room_name_exists(self,name:str) ->bool:
        self.in_process = True
        self.sock.send(pickle.dumps("is exist"))
        print('from check if room name exists')
        tmp = self.get_current_waiting_msg()
        self.sock.send(pickle.dumps(name))
        print('from check if room name exists')
        result = self.get_current_waiting_msg()
        self.in_process = False
        return result
    
    def get_room_by_id(self,id_num:int,name:str) ->chatroom:
        self.in_process = True
        self.sock.send(pickle.dumps(f"get room by id id:<{id_num}> name:<{name}>"))
        print('from get room by id')
        chat_room = self.get_large_data()
        print(f"server sent this as chatroom: {chat_room}")
        if not isinstance(chat_room,chatroom):
            self.in_process = False
            return False
        need_imgs_names = []
        for msg in chat_room.msgs:
            if not exists(f"pictures\\{msg.img_name}"):
                need_imgs_names.append(msg.img_name)
        if len(need_imgs_names) > 0:
            self.sock.send(pickle.dumps("need"))
            print('from get room by id')
            need_what = self.get_current_waiting_msg()
            self.sock.send(pickle.dumps(need_imgs_names))

            for img_name in need_imgs_names:
                self.get_picture_and_save(img_name)
        else:
            self.sock.send(pickle.dumps("no need"))

        self.in_process = False
        return chat_room
    
    def get_room_by_name_dict(self,name:str,room_name:str)->dict:
        self.sock.send(pickle.dumps(f"room name dict"))
        print("from get room by name")
        result_dict = self.get_large_data()
        try:
            return self.get_room_by_id(result_dict[room_name],name)
        except KeyError:
            return False


    def create_message_and_sent_to_server(self,name:str,msg:str,chat_room:chatroom,img_path_and_name:str,title:str):
        self.in_process = True
        if img_path_and_name != "":
            img_name = img_path_and_name[img_path_and_name.rfind("/")+1:]
        else:
            img_name = ""
        new_msg = message(name,msg,chat_room,img_name,title)
        self.sock.send(pickle.dumps("new msg"))
        print('from create_message_and_sent_to_server')
        send_msg = self.get_current_waiting_msg()
        self.sock.send(pickle.dumps(new_msg))
        time.sleep(0.5)
        self.sock.send("stop".encode())
        print('from create_message_and_sent_to_server')
        ok_msg = self.get_current_waiting_msg()
        if img_name != "":
            with open(img_path_and_name,'rb') as img:
                self.sock.send(img.read())
                time.sleep(0.5)
                self.sock.send("stop".encode())
        self.in_process = False

                
    def get_picture_and_save(self,img_name:str):
        img = b""
        while True:
            packet = self.sock.recv(1054)
            if packet == "stop".encode():
                break
            img+=packet
        with open(f"pictures\\{img_name}",'wb') as new_img:
            new_img.write(img)
    
    def send_and_recv_search_results(self,keyword:str) ->dict[chatroom:int]:
        self.in_process = True
        self.sock.send(pickle.dumps("search"))
        print('from send and recv search results')
        msg = self.get_current_waiting_msg()
        print(f"{msg} is what server said")
        self.sock.send(pickle.dumps(keyword))
        room_score_dict = self.get_large_data()
        print(room_score_dict)
        if room_score_dict == {}:
            return []
        room_score_dict = {k: v for k, v in sorted(room_score_dict.items(), key=lambda item: item[1])}
        result_dict = self.procces_room_score_dict(room_score_dict)

        self.in_process = False

        return result_dict

    def procces_room_score_dict(self,room_score_dict:dict[chatroom:int]) ->dict[chatroom:int]:
        final_dict = {}
        print(f"before precent {room_score_dict}")
        room_score_dict = self.make_dict_score_be_precent(room_score_dict)
        print(f"user controller: {room_score_dict}")
        if len(room_score_dict) > 20:
            look_for = 20
        else:
            look_for = len(room_score_dict)

        lst_of_keys = list(room_score_dict)
        needed_keys = lst_of_keys[-1*look_for:]
        for key in needed_keys:
            final_dict[key] = room_score_dict[key]
        return final_dict 
    
    def make_dict_score_be_precent(self,room_score_dict:dict[chatroom:int]) ->dict[chatroom:int]:
        all_values = room_score_dict.values()
        print(all_values)
        max_score = max(all_values)
        new_dict = {}
        for key in room_score_dict:
            try:
                new_dict[key] = room_score_dict[key]*100//max_score
            except ZeroDivisionError:
                new_dict[key] = room_score_dict[key]*100
        return new_dict
    
    def make_dict_score_be_precent_for_words(self,room_score_dict:dict[str:int]) ->dict[str:int]:
        all_values = room_score_dict.values()
        print(all_values)
        try:
            max_score = max(all_values)
        except ValueError:
            return {}
        new_dict = {}
        for key in room_score_dict:
            try:
                new_dict[key] = room_score_dict[key]*100//max_score
            except ZeroDivisionError:
                new_dict[key] = room_score_dict[key]*100
        return new_dict
    


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