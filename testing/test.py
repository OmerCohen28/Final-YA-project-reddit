'''from tkinter import *

master = Tk()

variable = StringVar(master)
variable.set("one") # default value

w = OptionMenu(master, variable, "one", "two", "three")
w.pack()

mainloop()'''

import datetime
from tkinter import  *
from tkinter import filedialog
from PIL import ImageTk,Image
import re
import pickle
from os.path import exists
from redis import *
#filename = filedialog.askopenfilename(filetypes=[('image files', '.png'), ('image files', '.jpg')], )
#print(filename)

#name = filename[filename.rfind("/")+1:]
#print(name)
x = {"4":5,5:3,"g":"f"}
for key in x:
    print(f"{key} {x[key]}")






