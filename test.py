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
import select
import rake_nltk
import nltk
#filename = filedialog.askopenfilename(filetypes=[('image files', '.png'), ('image files', '.jpg')], )
#print(filename)

#name = filename[filename.rfind("/")+1:]
#print(name)

#chat_room = pickle.loads(r.get('0'))
#print(chat_room.msgs[0].img_name)

from tkinter import Frame, Tk


s = "my name is omer and im here to say that omer is the omer of the omers"
r = rake_nltk.Rake("stop.txt")


lst = [1,2,3]
print(type(lst))