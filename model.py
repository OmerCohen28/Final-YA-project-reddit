import redis
import pickle
from classes.chatroom.chatroom import chatroom
from classes.user.user import User
class db:

    def __init__(self):
        self.r = redis.Redis()

    def insert_user(self,user:User) ->bool:
        if self.get_user(user.name) == "key didn't have a value":
            print("in")
            return self.r.set(str(user.name),pickle.dumps(user))
        else:
            return False

    def delete_user(self,name:str) ->bool:
        return self.r.delete(name)
    
    def get_user(self,name:str) ->User:
        try:
            return pickle.loads(self.r.get(str(name)))
        except TypeError:
            return "key didn't have a value"

    def insert_chat(self,id_num:int,chat :chatroom) ->bool:
        return self.r.set(str(id_num),pickle.dumps(chat))

    def get_chat(self,id_num:int) ->chatroom:
        try:
            return pickle.loads(self.r.get(id_num))
        except TypeError:
            return "key didn't have a velue"

    def set_current_chat_room_id(self,curr_free_id:int):
        self.r.set("chat id",str(curr_free_id))
    
    def get_current_chat_room_id(self):
        try:
            return int(self.r.get("chat id").decode())
        except:
            None

    def set_current_chat_name_to_id_dict(self,curr_dict):
        self.r.set("name to id dict",pickle.dumps(curr_dict))
    
    def get_current_chat_name_to_id_dict(self):
        try:
            return pickle.load(self.r.get("name to id dict"))
        except:
            return None


db_conn = db()
print((db_conn.get_chat(0)))
    