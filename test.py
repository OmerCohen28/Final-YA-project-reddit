from chatroom.chatroom import *

th = chatroom("omer",['gay'],4,["fuck"],['omer'])

th.admins_list.append("omer")

th.make_admin("benny")

print(th.admins_list)

print(th.room_id)