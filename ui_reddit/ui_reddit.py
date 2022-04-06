from tkinter import *
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
        frame_btn = Frame(self.root)
        frame_entry1 = Frame(self.root)
        frame_entry2 = Frame(self.root)

        welcome_lbl = Label(self.root, text="Welcome to the coolest reddit clone you will find on the internet!",font=("Arial",15))

<<<<<<< HEAD

        #self.img = ImageTk.PhotoImage(PIL.Image.open('logo.png'))
        #img_lbl = Label(self.root,image=self.img,borderwidth=0)
        self.pic = PhotoImage(file='logo.png')
        lbl = Label(left_frame,image=self.pic)
        self.root.wm_attributes('-transparentcolor','white')
        lbl.pack()
=======
        login_btn = self.make_log_in_button(frame_btn)
        signup_btn = self.make_sign_up_button(frame_btn)
        guest_btn = Button(frame_btn,text="Continue As a Guess",command=self.Do,font=("Arial",11))
>>>>>>> parent of 617c280 (still needs to be changed)

        self.img = ImageTk.PhotoImage(PIL.Image.open('logo.png'))
        img_lbl = Label(self.root,image=self.img,borderwidth=0)

        name_entry_var = StringVar()
        password_entry_var = StringVar()
        name_entry = Entry(frame_entry1,textvariable=name_entry_var,font=("Arial",15))
        password_entry = Entry(frame_entry2,textvariable=password_entry_var,font=("Arial",15))
        name_lbl = Label(frame_entry1,text="Username:",font=("Arial",15))
        password_lbl = Label(frame_entry2,text="Password:",font=("Arial",15))

        welcome_lbl.pack(pady=5)
        img_lbl.pack()
        name_lbl.pack(side=LEFT)
        name_entry.pack(side=LEFT)
        password_lbl.pack(side=LEFT)
        password_entry.pack(side=LEFT)
        login_btn.pack(side=LEFT,anchor=N,padx=7)
        signup_btn.pack(side=LEFT,anchor=N,padx=7)
        guest_btn.pack(side=LEFT,padx=7)
        frame_entry1.pack()
        frame_entry2.pack(pady=5)
        frame_btn.pack()


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