from tkinter import *
from tkinter import font
from tkinter import messagebox
import PIL
from PIL import ImageTk
import pickle
from user_controller import user_controller
import time

class ui_reddit:

    def __init__(self,root:Tk):
        self.root = root
        self.root.protocol("WM_DELETE_WINDOW",self.handle_close)
        self.root.title("Reddit Clone")
        self.user_controller = user_controller()

    #clear the screen
    def clear_screen(self) ->None:
        for widget in self.root.winfo_children():
            widget.destroy()

    def handle_close(self):
        self.user_controller.close_sock()
        messagebox.showinfo(message="Thanks for being here")
        self.root.destroy()

    '''
    main functions - 
    - main_menu_screen()
    - log_in_screen()
    - sign_up_screen()
    - in_chat_screen()
    - comment_section_screen()

    all other functions are supportive functions of these 4 main ones
    '''

    #screen that shows chat_rooms you've joined, if you haven't joined any it'll suggest you to join some
    #also shows some user and social info, have to think what
    def main_menu_screen(self):
        self.clear_screen()
        lbl = Label(self.root,text=self.user.name)
        lbl.pack()


    '''
    the next following functions are almost identical, this way you can just back and forth in the signup/login without much
    ui change, i wouldn't want to make a new ui for login/signup i think they should be the same
    '''
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
        log_in = Label(lbl_frame,text="Log In",font=("arial",25),bg="white")
        name_lbl = Label(lbl_frame,text="Username:",font=("Arial",15),bg="white")
        self.name_entry_log_in = Entry(lbl_frame,font=("Arial",15))
        password_lbl = Label(lbl_frame,text="Password:",font=("Arial",15),bg="white")
        self.password_entry_log_in = Entry(lbl_frame,font=("Arial",15))

        log_in.grid(column=0,row=0)
        space_lbl2.grid(column=0,row=1)
        space_lbl.grid(column=0,row=3)
        name_lbl.grid(column=0,row=2)
        self.name_entry_log_in.grid(column=1,row=2)
        password_lbl.grid(column=0,row=4)
        self.password_entry_log_in.grid(column=1,row=4)

        #buttons_frame
        button_frame = Frame(right_frame,bg="white")
        help_frame = Frame(button_frame)
        log_in_btn = Button(button_frame,text="Log In",bg="#6666ff",fg="white",command=self.send_log_in_info,font=("Arial",15),width=30,height=1)
        msg_lbl = Label(button_frame,text="Don't have an account yet?",font=("Arial",10),bg="white")
        sign_up_btn = Button(button_frame,text="Sign Up",bg="white",fg="#6666ff",font=("Arial",10,font.BOLD),borderwidth=0,command=self.change_to_signup)
        continue_as_a_guest_btn = Button(right_frame,text="Or continue as a guest",font=("Arial",10,font.BOLD),bg="white",fg="#6666ff",borderwidth=0)

        log_in_btn.pack()
        msg_lbl.pack(side=LEFT,pady=10)
        sign_up_btn.pack(side=LEFT,pady=10)
        help_frame.pack(side=BOTTOM)

        lbl_frame.pack(pady=50)
        button_frame.pack()
        continue_as_a_guest_btn.pack(anchor=W,padx=30)


        left_frame.pack(side=LEFT,expand=TRUE,fill=BOTH)
        right_frame.pack(side=RIGHT,expand=TRUE,fill=BOTH)

    #sign-up screen
    def sign_up_screen(self):
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
        self.name_entry_sign_up = Entry(lbl_frame,font=("Arial",15))
        password_lbl = Label(lbl_frame,text="Password:",font=("Arial",15),bg="white")
        self.password_entry_sign_up = Entry(lbl_frame,font=("Arial",15))

        sign_up.grid(column=0,row=0)
        space_lbl2.grid(column=0,row=1)
        space_lbl.grid(column=0,row=3)
        name_lbl.grid(column=0,row=2)
        self.name_entry_sign_up.grid(column=1,row=2)
        password_lbl.grid(column=0,row=4)
        self.password_entry_sign_up.grid(column=1,row=4)

        #buttons_frame
        button_frame = Frame(right_frame,bg="white")
        help_frame = Frame(button_frame)
        sign_up_btn = Button(button_frame,text="Sign Up",bg="#6666ff",fg="white",command=self.send_sign_up_info,font=("Arial",15),width=30,height=1)
        msg_lbl = Label(button_frame,text="Already have an account?",font=("Arial",10),bg="white")
        log_in_btn = Button(button_frame,text="Log in",bg="white",fg="#6666ff",font=("Arial",10,font.BOLD),borderwidth=0,command=self.change_to_login)
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


    #log in/sign up function group

    def Do(self):
        pass

    def send_log_in_info(self):
        msg,user = self.user_controller.log_in(self.name_entry_log_in.get(),self.password_entry_log_in.get())
        if(msg == "no username"):
            messagebox.showerror(title="Log in failed",message="The username you enterd was inccorect, try again")     
        elif(msg=="password is inccorect"):
            messagebox.showerror(title="Log in failed",message="The password you enterd was inccorect, try again")        
        else:
            self.user = user
            self.main_menu_screen()

    def send_sign_up_info(self):
        is_ok = self.user_controller.sign_up(self.name_entry_sign_up.get(),self.password_entry_sign_up.get(),False)
        if(not is_ok):
            messagebox.showerror(title="Username is in use",message="Sorry, this username is already taken, please try another one")
        else:
            self.log_in_screen()

    def easter_egg(self):
        messagebox.showinfo(title="easter egg!",message="Wow you discoverd an easter egg. This is Rick Sanchez from the great TV show Rick and Morty")

    def change_to_login(self):
        self.log_in_screen()
    
    def change_to_signup(self):
        self.sign_up_screen()

rot = Tk()

ui = ui_reddit(rot)

ui.log_in_screen()

rot.mainloop()