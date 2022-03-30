import redis
import pickle
class db:

    def __init__(self,r:redis.Redis):
        self.r = r

    def insert_user(self,name:str,user):
        return self.r.set(name,pickle.dumps(user))

    def delete_user(self,name:str):
        return self.r.delete(name)
    
    def get_user(self,name:str):
        try:
            return pickle.loads(self.r.get(name))
        except TypeError:
            return "key didn't have a value"

    def insert_chat(self,id_num:int,chatroom):
        pass

r = redis.Redis()
db_r = db(r)
print('started')
print(db_r.insert_user('benny','yakub'))
print(db_r.get_user('benny'))
print(db_r.insert_user('benny','yaya'))
print(db_r.delete_user('benny'))
print(db_r.get_user('benny'))
