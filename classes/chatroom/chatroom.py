import time
from classes.user.user import User

class chatroom:

    def __init__(self,creator:User,name:str, topcis,room_id:int, banned_words):
        self.creator = creator
        self.name = name
        self.topcis = topcis
        self.admins_list = [creator]
        self.members = [creator]
        #self.create_time #add a way to know when it was created
        self.room_id = room_id
        self.common_words = []
        self.banned_words = banned_words
        self.msgs = []

    def kick(self,user:User) ->bool:
        try:
            del self.members[self.members.index(user)]
            return True
        except:
            return False


    def add_user(self,user:str) ->bool:
        try:
            self.members.append(user)
            return True
        except:
            return False

    def make_admin(self,user:str) ->None:
        self.admins_list.append(user)

    def add_msg(self,msg):
        self.msgs.append(msg)


