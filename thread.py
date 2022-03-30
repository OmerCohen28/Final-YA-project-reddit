import time
class Thread:

    def __init__(self,creator:str, topcis:list[str],room_id:int, banned_words:list[str]):
        self.creator = creator
        self.topcis = topcis
        self.admins_list = []
        self.members = []
        #self.create_time #add a way to know when it was created
        self.room_id = room_id
        self.common_words = []
        self.banned_words = banned_words