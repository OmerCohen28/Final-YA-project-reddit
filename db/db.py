import redis
import pickle
from chatroom.chatroom import chatroom
from user.user import User
class db:

    def __init__(self):
        self.r = redis.Redis()

    def insert_user(self,user:User) ->bool:
        return self.r.set(str(user.id_num),pickle.dumps(user))

    def delete_user(self,id_num:str) ->bool:
        return self.r.delete(id_num)
    
    def get_user(self,id_num:str) ->User/str:
        try:
            return pickle.loads(self.r.get(str(id_num)))
        except TypeError:
            return "key didn't have a value"

    def insert_chat(self,id_num:int,chat :chatroom) ->bool:
        return self.r.set(str(id_num),pickle.dumps(chat))

    def get_chat(self,id_num:int) ->chatroom/str:
        try:
            return pickle.loads(self.r.get(id_num))
        except TypeError:
            return "key didn't have a velue"


