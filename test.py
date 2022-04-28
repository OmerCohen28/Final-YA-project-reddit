'''from tkinter import *

master = Tk()

variable = StringVar(master)
variable.set("one") # default value

w = OptionMenu(master, variable, "one", "two", "three")
w.pack()

mainloop()'''

import datetime
from distutils import extension
import keyword
from socket import AF_INET, SOCK_STREAM,socket
from tkinter import  *
from tkinter import filedialog
from PIL import ImageTk,Image
import re
import pickle
from os.path import exists
from redis import *
from classes.chatroom.chatroom import chatroom
from classes.server.server import server
from classes.user.user import User
from model import db
import select
import rake_nltk
import nltk
import re
#filename = filedialog.askopenfilename(filetypes=[('image files', '.png'), ('image files', '.jpg')], )
#print(filename)

#name = filename[filename.rfind("/")+1:]
#print(name)
r = Redis()
use = pickle.loads(r.get("0"))
ooo = pickle.loads(r.get("omer"))
members = use.members
print(int("1"))
x = "73534789x"
pat = re.compile(r"^\d+$")
result = re.findall(pattern=pat,string = x)

if len(result) != 1:
    print("no")
else:
    print("yes")





'''dict_test = {}
for key in x:
    dict_test[key] = x[key]
print(dict_test)
dict_test = {k: v for k, v in sorted(dict_test.items(), key=lambda item: item[1])}
print(dict_test)
print(len(dict_test))
print(dict_test[10:])'''