'''from tkinter import *

master = Tk()

variable = StringVar(master)
variable.set("one") # default value

w = OptionMenu(master, variable, "one", "two", "three")
w.pack()

mainloop()'''

import datetime
from distutils import extension
from tkinter import  *
from tkinter import filedialog
from PIL import ImageTk,Image
import re
import pickle
from os.path import exists
from redis import *
from classes.chatroom.chatroom import chatroom
#filename = filedialog.askopenfilename(filetypes=[('image files', '.png'), ('image files', '.jpg')], )
#print(filename)

#name = filename[filename.rfind("/")+1:]
#print(name)

#chat_room = pickle.loads(r.get('0'))
#print(chat_room.msgs[0].img_name)

from tkinter import Frame, Tk

class MyApp():
    def __init__(self):
        self.root = Tk()
        self.root.geometry("600x600")
        s=""
        for i in range(53):
            s+="x"
        lbl1 = Label(text=s,font=("Arial",12))
        lbl1.pack()
        lbl2 = Label(text="",bg="red",width=53)
        lbl2.pack()
        self.root.mainloop()

if __name__ == '__main__':
    app = MyApp()




