from user.user import *
from db.db import *
from socket import *
from chatroom.chatroom import *

db_conn = db()

use = User("omer",'123','123',True,socket())

chat = chatroom('omer',['nothing'],1234,['fuck'],['me'])

db_conn.insert_chat(chat.room_id,chat)

chat_2 = db_conn.get_chat(1234)

print(chat_2.room_id)

use.join_room(1234,db_conn)

print(use.joined_room[0].creator)
