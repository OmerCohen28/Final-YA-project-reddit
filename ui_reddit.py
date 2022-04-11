from functools import partial
from pydoc_data.topics import topics
from re import L
from tkinter import *
from tkinter import font
from tkinter import messagebox
import PIL
from PIL import ImageTk
import pickle
from classes.chatroom.chatroom import chatroom
from classes.message.message import message
from classes.user.user import User
from user_controller import user_controller
import time
class ui_reddit:

    def __init__(self,root:Tk):
        self.root = root
        self.root.protocol("WM_DELETE_WINDOW",self.handle_close)
        self.root.title("Reddit Clone")
        self.root.resizable(False,False)
        self.user_controller = user_controller()
        self.chat_img_lst = []
        self.chat_img_lst_index=0
        self.expand_msg_img_lst = []
        self.expand_msg_ing_lst_index=0

    #general purpose functions

    def clear_screen(self) ->None:
        for widget in self.root.winfo_children():
            widget.destroy()

    def handle_close(self):
        self.user_controller.close_sock()
        messagebox.showinfo(message="Thanks for being here")
        self.root.destroy()

    def create_top_frame(self):
        frame = Frame(self.root,bg="#6699ff")

        lbl = Label(frame,text = "Reddit Clone",font=("Arial",15),bg="#6699ff",fg="white")
        self.logo_img = PhotoImage(file='reddit-logo.png')
        menu_btn = Button(frame,image=self.logo_img,borderwidth=0,bg="#6699ff",command=self.main_menu_screen)
        #user_drop_down = self.user_drop_down(frame)
        self.search_bar = Entry(frame,font=("Arial",15),bg="#3399ff",fg = "white")
        self.search_bar.config(width=30)

        menu_btn.pack(side=LEFT,padx=10)
        lbl.pack(side=LEFT,padx=10)
        self.search_bar.pack(side=LEFT,padx=100)
        #user_drop_down.pack(side=LEFT,padx=10)
        return frame

    def expand_message(self,msg:message):
        self.clear_screen()
        print("oedfjkpo")
        color = "#6666ff"
        self.root.config(bg=color)
        top_frame = self.create_top_frame()
        top_frame.config(height=350)
        top_frame.pack(side=TOP,fill=X)

        #creating scrolling comment section
        main_frame = Frame(self.root,bg="#6666ff")
        canvas = Canvas(main_frame,width="10",bg="#6666ff")
        scroll_bar = Scrollbar(main_frame,orient=VERTICAL,command=canvas.yview)
        canvas.configure(yscrollcommand=scroll_bar.set)
        canvas.bind("<Configure>",lambda event: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.bind_all("<MouseWheel>",lambda e:self.on_mousewheel(e,canvas))
        second_frame = Frame(canvas,bg="#6666ff")
        canvas.create_window((400,0),window=second_frame,anchor=NW)
        comments_frame_lst = self.make_frame_chat_list(msg.comments,second_frame)
        for frame in comments_frame_lst:
            frame.pack(fill=X,pady=10,expand=TRUE)


        packing_frame = Frame(canvas,bg="#6666ff")

        sent_in_btn = Button(packing_frame,text = msg.sent_in.name, font=("Arial",12,font.ITALIC,font.BOLD),borderwidth=0,bg = color,fg="white")
        sent_by_lbl = Label(packing_frame,text = msg.sent_by,font=("Arial",12),bg=color,fg="white")
        time_lbl = Label(packing_frame,text =msg.time_str,font=("Arial",12),bg=color,fg="white")
        title_lbl = Label(packing_frame,text=msg.title,font=("Arial",15,font.BOLD),bg=color,fg="white")
        
        sent_in_btn.pack(side=TOP,anchor=W,pady=10)
        sent_by_lbl.pack(side=TOP,anchor=W,pady=5)
        time_lbl.pack(side=TOP,anchor=W,pady=5)
        title_lbl.pack(side=TOP,anchor=W,pady=20)

        lbl_lst = []
        holder_msg = msg.msg
        while len(holder_msg) >40:
            if(len(holder_msg[40:])>40):
                tmp_msg = holder_msg[:40]+" -"
            else:
                tmp_msg = holder_msg[:40]
            lbl_lst.append(Label(packing_frame,text=tmp_msg,font=("Arial",12),bg=color,fg="white"))
            holder_msg = holder_msg[40:]
        
        for lbl in lbl_lst:
            lbl.pack(side=TOP,anchor=W,pady=5)

        if msg.img_name!="no":
            try:
                print(msg.img_name)
                print("yop")
                self.expand_msg_img_lst.append(PhotoImage(file=msg.img_name))
                img_lbl = Label(packing_frame,image=self.expand_msg_img_lst[self.expand_msg_ing_lst_index],bg = color)
                img_lbl.pack(side=TOP,anchor=W,pady=5)
                self.expand_msg_ing_lst_index+=1                 
            except:
                print("sup")
                space_lbl = Label(packing_frame,height=4,text="",bg=color)
                space_lbl.pack(side=TOP,anchor=W,pady=5)

        comment_lbl = Label(self.root,text="Comments:",font=("Arial",15,font.BOLD),bg=color,fg="white")
        comment_lbl.pack(side=TOP,anchor=E,padx=300)



        packing_frame.pack(side=LEFT,anchor=N,pady=10)
        scroll_bar.pack(side=RIGHT,fill=Y)
        canvas.pack(fill=BOTH,expand=TRUE)
        main_frame.pack(fill=BOTH,expand=TRUE)

   
    def on_mousewheel(self,event,canvas):
        canvas.yview_scroll(-1*(event.delta//120), "units")

    def create_chatroom(self):
        toplevel = Toplevel()

        chat_name_lbl = Label(toplevel,text="Enter the name of the chatroom")
        chat_name_entry = Entry(toplevel)

        topic_lbl = Label(toplevel,text="Enter the main topic of the room, you can always change it later")
        topic_entry = Entry(toplevel)

        create_btn = Button(toplevel,text="Create Room!", command=lambda:self.mange_creating_new_room(chat_name_entry.get(),topic_entry.get(),toplevel))

        chat_name_lbl.grid(column=0,row=0,pady=10)
        chat_name_entry.grid(column=1,row=0,pady=10)
        topic_lbl.grid(column=0,row=1,pady=10)
        topic_entry.grid(column=1,row=1,pady=10)
        create_btn.grid(column=0,row=2,pady=15)

    def mange_creating_new_room(self,name,topic,toplevel):
        print(name)
        if self.user_controller.check_if_room_name_exists(name):
            messagebox.showerror(title="Room name already exists",message="Sorry but this room name is already in use")
        else:
            result = self.user_controller.create_new_room_with_server(self.user,name,topic)
            if result:
                toplevel.destroy()
            else:
                messagebox.showerror(title="Creating a room failed",message="The proccess you attempted has failed, try again")
 
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
        print("menu")
        lst = self.user_controller.get_msgs_for_main_menu()
        self.clear_screen()
        self.root.geometry("1150x800")
        self.root.configure(bg="white")
        top_frame = self.create_top_frame()
        top_frame.config(height=350)
        top_frame.pack(side=TOP,fill=X)

        
        #creating scrolling chat screen
        main_frame = Frame(self.root)
        canvas = Canvas(main_frame,width="10")
        scroll_bar = Scrollbar(main_frame,orient=VERTICAL,command=canvas.yview)
        canvas.configure(yscrollcommand=scroll_bar.set)
        canvas.bind("<Configure>",lambda event: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.bind_all("<MouseWheel>",lambda e:self.on_mousewheel(e,canvas))
        second_frame = Frame(canvas)
        canvas.create_window((350,0),window=second_frame,anchor=NW)

        packing_frame = Frame(canvas)

        user_info_frame = self.user_info(packing_frame)
        user_info_frame.pack(side=TOP,anchor=W,pady=20)

        user_actions_frame = self.user_actions(packing_frame)
        user_actions_frame.pack(side=TOP,anchor=W,pady=5)

        packing_frame.pack(side=LEFT,anchor=N,pady=10)



        frame_lst = self.make_frame_chat_list(lst,second_frame)

        for frame in frame_lst:
            frame.pack(fill=X,pady=10,expand=TRUE)

        packing_frame.pack(side=LEFT,anchor=N,pady=10)
        scroll_bar.pack(side=RIGHT,fill=Y)
        canvas.pack(fill=BOTH,expand=TRUE)
        main_frame.pack(fill=BOTH,expand=TRUE)



        
        
        
        


    '''
    the next following functions are almost identical, this way you can just back and forth in the signup/login without much
    ui change, i wouldn't want to make a new ui for login/signup i think they should be the same
    '''
    #log-in screen 
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


    #main menu screen functin groups
    def user_drop_down(self,frame):
        clicked = StringVar()
        options = ["Options","User Info","Change User Settings","Window Settings"]
        clicked.set(options[0])
        drop_down = OptionMenu(frame,clicked,*options,command=self.user_options)   
        drop_down.config(bg="#6666ff",fg="white")
        return drop_down

    def user_options(self,event):
        pass

    def make_frame_chat_list(self,lst:list[message],container_frame:Frame) ->list[Frame]:
        result = []
        self.expand_img = PhotoImage(file="maximize.png")
        count =0
        for msg in lst:
            if count % 2 == 0:
                color ="#6699ff"
            else:
                color = "#9999ff"

            frame = Frame(container_frame,bg = color,highlightbackground="black", highlightthickness=2)
            send_by_lbl = Label(frame,text = f"user: {msg.sent_by}",font=("Arial",12),bg = color)
            time_lbl = Label(frame,text = msg.time_str,font=("Arial",12),bg = color)
            sent_in_btn = Button(frame,text = msg.sent_in.name, font=("Arial",12,font.ITALIC,font.BOLD),borderwidth=0,bg = color)
            if(len(msg.title)>50):
                actual_title = msg.title[:50] + "..."
            else:
                actual_title = msg.title
            title_lbl = Label(frame,text = actual_title,font=("arial",15,font.BOLD),bg = color)
            if(len(msg.msg)>50):
                actual_msg = msg.msg[:50] + "..."
            else:
                actual_msg = msg.msg
            msg_lbl = Label(frame,text = actual_msg,font=("Arial",12),bg = color,height=3)
            expand_btn = Button(frame,image=self.expand_img,command=partial(self.expand_message,msg),borderwidth=0,bg = color)

            title_lbl.pack(side=TOP,anchor=E)
            expand_btn.pack(side=LEFT,anchor=N,pady=5,padx=3)
            sent_in_btn.pack(side=TOP,anchor=W,pady=5)
            send_by_lbl.pack(side=TOP,anchor=W,pady=5,padx=3)
            time_lbl.pack(side=TOP,anchor=W,pady=5,padx=3)
            msg_lbl.pack(pady=10,side=LEFT,anchor=S)


            if msg.img_name!="no":
                try:
                    self.chat_img_lst.append(PhotoImage(file=msg.img_name))
                    img_lbl = Label(frame,image=self.chat_img_lst[self.chat_img_lst_index],bg = color)
                    img_lbl.pack(pady=5)
                    self.chat_img_lst_index+=1                 
                except:
                    space_lbl = Label(frame,height=4,text="",bg=color)
                    space_lbl.pack(pady=2,side=TOP)
            else:
                space_lbl = Label(frame,height=4,text="",bg=color)
                space_lbl.pack(pady=2,side=TOP)
            count+=1
            result.append(frame)
        return result

        
    def user_info(self,container_frame):
        frame = Frame(container_frame,bg="#6666ff")
        name_lbl = Label(frame,text=f"You are viewed as {self.user.name}",bg="#6666ff",fg="white",font=("Arial",15))
        joined_lbl = Label(frame,text=f"You have currently joined {len(self.user.joined_room)} rooms",bg="#6666ff",fg="white",font=("Arial",15))
        admin_lbl = Label(frame,text=f"You are currently admin at {len(self.user.admin_in)} rooms",bg="#6666ff",fg="white",font=("Arial",15))

        name_lbl.pack(side=TOP,anchor=W)
        joined_lbl.pack(side=TOP,anchor=W)
        admin_lbl.pack(side=TOP,anchor=W)

        return frame
    
    def user_actions(self,container_frame):
        frame = Frame(container_frame,bg="#6666ff")
        msg_lbl = Label(frame,text="User Options:",font=("Arial",15,font.BOLD),bg="#6666ff",fg="white")
        change_username_btn = Button(frame,text="Change username",command=self.Do,font=("Arial",15,font.ITALIC,font.BOLD),bg="#6666ff",fg="white",borderwidth=0)
        change_password_btn = Button(frame,text="Change password",command=self.Do,font=("Arial",15,font.ITALIC,font.BOLD),bg="#6666ff",fg="white",borderwidth=0)
        join_room_by_id_btn = Button(frame,text="Join room by his ID",command=self.Do,font=("Arial",15,font.ITALIC,font.BOLD),bg="#6666ff",fg="white",borderwidth=0)
        create_chat_room_btn = Button(frame,text="Create Room",command=self.create_chatroom,font=("Arial",15,font.ITALIC,font.BOLD),bg="green",borderwidth=0)
        
        msg_lbl.pack(side=TOP)
        create_chat_room_btn.pack(side=TOP)
        join_room_by_id_btn.pack(side=TOP)
        change_username_btn.pack(side=TOP)
        change_password_btn.pack(side=TOP)
        return frame


rot = Tk()

ui = ui_reddit(rot)

ui.log_in_screen()

rot.mainloop()