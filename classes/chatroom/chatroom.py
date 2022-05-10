import datetime
from classes.user.user import User

class chatroom:

    def __init__(self,creator:User,name:str, room_id:int, banned_words):
        self.creator = creator
        self.name = name
        self.current_members = 0
        self.members = [creator]
        self.room_id = room_id
        self.common_words = {}
        self.removed_common_words = []
        self.banned_words = banned_words
        self.msgs = []
        self.last_sent_time = datetime.datetime.now()
        self.create_time = datetime.datetime.now()

       
    

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

    def add_msg(self,msg):
        self.msgs.append(msg)


