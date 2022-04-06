from tkinter import *
from tkinter import font
from tkinter import messagebox
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
        self.root.geometry("800x450")
        left_frame = Frame(self.root,bg="#6666ff")
        right_frame = Frame(self.root,bg="white")

        #left frame
        self.pic = PhotoImage(file='logo.png')
        btn = Button(left_frame,image=self.pic,borderwidth=0,command=self.easter_egg)

        msg1 = Label(left_frame,text="Welcome to the coolest reddit clone",font=("arial",15,font.BOLD),bg="#6666ff",fg="white")
        msg2 = Label(left_frame,text="you will find on the internet!",font=("arial",15,font.BOLD),bg="#6666ff",fg="white")

        btn.pack(pady=20)
        msg1.pack(pady=5)
        msg2.pack(pady=3)

        #right frame

        #lbl_frame
        lbl_frame = Frame(right_frame,bg="white")
        space_lbl = Label(lbl_frame,bg="white")
        space_lbl2 = Label(lbl_frame,bg="white")
        sign_up = Label(lbl_frame,text="Sign Up",font=("arial",25),bg="white")
        name_lbl = Label(lbl_frame,text="Username:",font=("Arial",15),bg="white")
        name_entry = Entry(lbl_frame,font=("Arial",15))
        password_lbl = Label(lbl_frame,text="Password:",font=("Arial",15),bg="white")
        password_entry = Entry(lbl_frame,font=("Arial",15))

        sign_up.grid(column=0,row=0)
        space_lbl2.grid(column=0,row=1)
        space_lbl.grid(column=0,row=3)
        name_lbl.grid(column=0,row=2)
        name_entry.grid(column=1,row=2)
        password_lbl.grid(column=0,row=4)
        password_entry.grid(column=1,row=4)

        #buttons_frame
        button_frame = Frame(right_frame,bg="white")
        help_frame = Frame(button_frame)
        sign_up_btn = Button(button_frame,text="Sign Up",bg="#6666ff",fg="white",command=self.Do,font=("Arial",15),width=30,height=1)
        msg_lbl = Label(button_frame,text="Already have an account?",font=("Arial",10),bg="white")
        log_in_btn = Button(button_frame,text="Log in",bg="white",fg="#6666ff",font=("Arial",10,font.BOLD),borderwidth=0)
        continue_as_a_guest_btn = Button(right_frame,text="Or continue as a guest",font=("Arial",10,font.BOLD),bg="white",fg="#6666ff",borderwidth=0)

        sign_up_btn.pack()
        msg_lbl.pack(side=LEFT,pady=10)
        log_in_btn.pack(side=LEFT,pady=10)
        help_frame.pack(side=BOTTOM)

        lbl_frame.pack(pady=50)
        button_frame.pack()
        continue_as_a_guest_btn.pack(anchor=W,padx=30)


        left_frame.pack(side=LEFT,expand=TRUE,fill=BOTH)
        right_frame.pack(side=RIGHT,expand=TRUE,fill=BOTH)



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

    def easter_egg(self):
        messagebox.showinfo(title="easter egg!",message="Wow you discoverd an easter egg. This is Rick Sanchez from the great TV show Rick and Morty")


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