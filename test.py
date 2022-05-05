import datetime
from socket import SOCK_DGRAM, socket
from tkinter import  *
from tkinter import filedialog
from PIL import ImageTk,Image
import re
import pickle
from redis import *
from classes.chatroom.chatroom import chatroom
from classes.user.user import User
import re
import time
import sys
import select
import rake_nltk
import nltk
#filename = filedialog.askopenfilename(filetypes=[('image files', '.png'), ('image files', '.jpg')], )
#print(filename)

import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar, DateEntry

'''
important thingy
'''
def example1():
    def print_sel():
        print(cal.selection_get())

    top = tk.Toplevel(root)

    cal = Calendar(top,
                   font="Arial 14", selectmode='day',
                   cursor="hand1", year=2018, month=2, day=5)
    cal.pack(fill="both", expand=True)
    ttk.Button(top, text="ok", command=print_sel).pack()

def example2():
    top = tk.Toplevel(root)

    ttk.Label(top, text='Choose date').pack(padx=10, pady=10)

    cal = DateEntry(top, width=12, background='darkblue',
                    foreground='white', borderwidth=2)
    cal.pack(padx=10, pady=10)

root = tk.Tk()

s = ttk.Style(root)
s.theme_use('clam')

ttk.Button(root, text='Calendar', command=example1).pack(padx=10, pady=10)
ttk.Button(root, text='DateEntry', command=example2).pack(padx=10, pady=10)
#root.mainloop()

r = Redis()

user = pickle.loads(r.get("omer"))
user.is_sys_admin = True
r.set("omer",pickle.dumps(user))
sys.exit()
print(chat.password)
chat.is_sys_admin = True

