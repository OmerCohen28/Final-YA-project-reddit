import time
class chatroom:

    def __init__(self,creator:str, topcis:list[str],room_id:int, banned_words:list[str], members:list[str]):
        self.creator = creator
        self.topcis = topcis
        self.admins_list = []
        self.members = members
        #self.create_time #add a way to know when it was created
        self.room_id = room_id
        self.common_words = []
        self.banned_words = banned_words

    def kick(self,user:str):
        pass  


    def add_user(self,user:str):
        pass

    def make_admin(self,user:str):
        self.admins_list.append(user)
    
    

