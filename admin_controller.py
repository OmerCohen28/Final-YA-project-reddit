from socket import *
from classes.chatroom.chatroom import chatroom
from user_controller import user_controller
import pickle

class admin_controller():
    def __init__(self):
        self.user_controller = user_controller()
    
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
        pass

    

admin = admin_controller()
lst = admin.return_all_rooms_sorted_by_members()

for chat_room in lst:
    print(chat_room)
    print(len(chat_room.members))