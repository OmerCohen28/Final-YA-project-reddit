
from classes.chatroom.chatroom import chatroom

from classes.chatroom.chatroom import chatroom
import datetime
class message:

    def __init__(self,sent_by:str,comments:list[str],msg:str,sent_in:chatroom,img_name:str,title:str):
        self.sent_by = sent_by
        self.comments = comments
        self.msg = msg
        self.sent_in = sent_in
        x = datetime.datetime.now()
        self.time_str = f"{x.day}/{x.month} {x.hour}:{x.minute}"
        self.img_name = img_name
        self.title = title
