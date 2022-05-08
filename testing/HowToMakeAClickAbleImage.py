import redis
import pickle
r = redis.Redis()

user = pickle.loads(r.get("ayal"))

user.is_sys_admin = True

r.set("ayal",pickle.dumps(user))
