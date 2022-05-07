from socket import *
from turtle import update
from classes.chatroom.chatroom import chatroom
from user_controller import user_controller
import pickle
import time
import datetime

class admin_controller():
    def __init__(self):
        self.user_controller = user_controller()
        self.get_current_days_to_skip()
    
    def show_all_rooms_by_key_word(self,keyword:str):
        return self.user_controller.send_and_recv_search_results(keyword)
    
    def get_all_rooms_from_server(self):
        self.user_controller.sock.send(pickle.dumps("chat id"))
        curr_chat_id = self.user_controller.get_current_waiting_msg()

        chat_room_lst = []
        for id_num in range(curr_chat_id):
            chat_room = self.user_controller.get_room_by_id(id_num,"no")
            chat_room_lst.append(chat_room)

        return chat_room_lst

    def return_all_rooms_sorted_by_members(self)->list[chatroom]:
        lst = self.get_all_rooms_from_server()
        print(lst)
        lst.sort(key=lambda x: len(x.members), reverse=True)
        return lst
    
    def get_all_current_users(self):
        self.user_controller.sock.send(pickle.dumps("get all users time dict"))
        user_time_dict = self.user_controller.get_large_data()
        print("uset time dict:",user_time_dict)
        now = datetime.datetime.now()

        updated_dict = {}

        for key in user_time_dict:
            updated_dict[key] = now-user_time_dict[key]
        
        return updated_dict
    
    def get_user_chat_room_dict(self):
        self.user_controller.sock.send(pickle.dumps("get all users chatroom dict"))
        user_chat_room_dict = self.user_controller.get_large_data()
        print(user_chat_room_dict)
        return user_chat_room_dict
    
    def change_date_of_server(self,days_to_skip):
        self.user_controller.sock.send(pickle.dumps(f"add days days:<{days_to_skip}>"))
        time.sleep(0.5)
        self.get_current_days_to_skip()
    
    def get_current_days_to_skip(self):
        self.user_controller.sock.send(pickle.dumps("get current days to skip"))
        days_to_skip = self.user_controller.get_current_waiting_msg()
        print("days to skip",days_to_skip)
        print(type(days_to_skip))
        try:
            self.days_to_skip = int(days_to_skip) 
        except TypeError:
            self.days_to_skip=0

    def set_a_message_for_user(self,msg:str,name:str):
        self.user_controller.sock.send(pickle.dumps(f"msg for user msg:<{msg}> name:<{name}>"))
        result = self.user_controller.get_current_waiting_msg()
        return result
    

