import redis
import pickle
r = redis.Redis()

user = pickle.loads(r.get("omer"))

user.is_sys_admin = True

r.set("omer",pickle.dumps(user))
