from telnetlib import EXOPL
from tkinter import *
from turtle import bgcolor
import PIL
from PIL import ImageTk
import pickle
import os
#To Do - display Images in chatroom!!!

class ui_reddit:

    def __init__(self,root:Tk):
        self.root = root
        self.root.title("Reddit Clone")

    #clear the screen
    def clear_screen(self) ->None:
        for widget in self.root.winfo_children():
            widget.destroy()


    '''
    main functions - 
    - main_menu_screen()
    - log_in_screen()
    - in_chat_screen()
    - comment_section_screen()

    all other functions are supportive functions of these 4 main ones
    '''

    #screen that shows chat_rooms you've joined, if you haven't joined any it'll suggest you to join some
    #also shows some user and social info, have to think what
    def main_menu_screen(self):
        pass

    #log-in screen for poeple to sign in/log-in as guests
    def log_in_screen(self):
        self.clear_screen()
        self.root.geometry("600x420")

        left_frame = Frame(self.root,bg ="#9966ff")
        right_frame = Frame(self.root)

        pic = PhotoImage(file='logo.png')
        lbl = Label(left_frame,image=pic)
        lbl.pack()

        right_frame.pack(side=RIGHT,expand=TRUE,fill=BOTH)
        left_frame.pack(side=LEFT,expand=TRUE,fill=BOTH)



    #shows the listbox of the chat + some other fetures
    #make it an option to click on a certain message and comment on it
    def in_chat_screen(self):
        pass

    #screen after clicking on a message, maybe open a whole new screen or maybe change the current one
    #shows comments on a message
    def comment_section_screen(self):
        pass 


    #log in function group

    def Do(self):
        pass


    def make_log_in_button(self,frame)->Button:
        self.login_img = PhotoImage(file=("login.png"))
        login_btn = Button(frame,image=self.login_img,command=self.Do,borderwidth=0)
        return login_btn

    def make_sign_up_button(self,frame)->Button:
        self.signup_img = PhotoImage(file=os.path.abspath("signup.png"))
        signup_btn = Button(frame,image=self.signup_img,command=self.Do,borderwidth=0)
        return signup_btn


rot = Tk()
ui = ui_reddit(rot)
ui.log_in_screen()
rot.mainloop()