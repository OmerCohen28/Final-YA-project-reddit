from cmath import phase
from functools import partial
from re import I
from tkinter import *
from tkinter import font
from tkinter import messagebox
from tkinter import filedialog
from PIL import ImageTk,Image
import pickle
from classes.chatroom.chatroom import chatroom
from classes.message.message import message
from classes.user.user import User
from user_controller import user_controller
import time
import _thread

class ui_reddit:
    def __init__(self,root:Tk):
        self.root = root
        self.root.protocol("WM_DELETE_WINDOW",self .handle_close)
        self.root.title("Reddit Clone")
        self.root.resizable(False,False)
        self.user_controller = user_controller()
        self.chat_img_lst = []
        self.chat_img_lst_index=0
        self.expand_msg_img_lst = []
        self.expand_msg_ing_lst_index=0
        self.current_chat_id = 0


    #general purpose functions
    def refresh_chat_room(self):
        while True:
            time.sleep(1)
            self.user_controller.get_refresh_notification()
            if self.user_controller.refresh:
                print("need refresh")
                self.refresh_btn.pack(side=TOP,anchor=E,pady=10)
                self.user_controller.refresh = False

    def clear_screen(self) ->None:
        for widget in self.root.winfo_children():
            widget.destroy()

    def handle_close(self):
        try:
            self.user_controller.close_connection(self.user.name)
        except AttributeError:
            self.user_controller.close_connection("guest")
        messagebox.showinfo(message="Thanks for being here")
        self.root.destroy()

    def create_top_frame(self):
        frame = Frame(self.root,bg="#6699ff")

        lbl = Label(frame,text = "Reddit Clone",font=("Arial",17,font.BOLD),bg="#6699ff")
        self.logo_img = ImageTk.PhotoImage(Image.open('program_pics\\reddit-logo.png'))
        menu_btn = Button(frame,image=self.logo_img,borderwidth=0,bg="#6699ff",command=self.main_menu_screen)
        
        if self.user.is_sys_admin:
            user_info_lbl = Label(frame,text=f"User: {self.user.name} (admin), Rooms: {len(self.user.joined_room)}",bg="#6699ff",font=("Arial",15))
        else:
            user_info_lbl = Label(frame,text=f"User: {self.user.name} , Rooms: {len(self.user.joined_room)}",bg="#6699ff",font=("Arial",15))
        
        space_lbl = Label(frame,text="",bg="#6699ff")

        space_lbl.pack(side=LEFT,anchor=S)
        menu_btn.pack(side=LEFT,padx=10)
        lbl.pack(side=LEFT,padx=10)
        user_info_lbl.pack(side=RIGHT,padx=10,pady=5,anchor=S)
        return frame

    def expand_message(self,msg:message):
        self.clear_screen()
        color = "#6666ff"
        self.root.config(bg="white")
        top_frame = self.create_top_frame()
        top_frame.config(height=350)
        top_frame.pack(side=TOP,fill=X)

        #creating scrolling comment section
        main_frame = Frame(self.root,bg="white")
        canvas = Canvas(main_frame,width="10",bg="white")
        scroll_bar = Scrollbar(main_frame,orient=VERTICAL,command=canvas.yview)
        canvas.configure(yscrollcommand=scroll_bar.set)
        canvas.bind("<Configure>",lambda event: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.bind_all("<MouseWheel>",lambda e:self.on_mousewheel(e,canvas))
        second_frame = Frame(canvas,bg="white")
        canvas.create_window((200,0),window=second_frame,anchor=NW)
        comments_frame_lst = self.make_frame_chat_list(msg.comments,second_frame)





        msg_frame = Frame(second_frame,bg="white")
        space_lbl = Label(msg_frame,text="",bg="white",width=100)
        space_lbl.pack()

        title_lbl = Label(msg_frame,bg=color,fg="white",text=msg.title,font=("Arial",20,font.BOLD),width=50)
        title_lbl.pack(side=TOP,pady=10)

        info_frame = Frame(msg_frame,highlightbackground="#0066ff", highlightthickness=2,bg="white",width=100)
        room_btn = Button(info_frame,text=f"Room/{msg.sent_in.name}",font=("Arial",15),bg="white",command=lambda:self.manage_join_room_by_id(msg.sent_in.room_id))
        created_by_lbl = Label(info_frame,text=f"Created by {msg.sent_by}",font=("Arial",15),bg="white")
        created_on_lbl = Label(info_frame,text=f"Created on {msg.time_str}",font=("Arial",15),bg="white")
        space_lbl2 = Label(info_frame,text="",bg="white",width=120)
        room_btn.pack(side=TOP,anchor=W,pady=10,padx=5)
        space_lbl2.pack(side=TOP,pady=10)
        created_by_lbl.pack(side=TOP,anchor=W,pady=10,padx=5)
        created_on_lbl.pack(side=TOP,anchor=W,pady=10,padx=5)
        info_frame.pack(side=TOP,pady=10)

        actual_msg_frame = Frame(msg_frame,bg="white",highlightbackground="#0066ff", highlightthickness=2)
        space_lbl3 = Label(actual_msg_frame,text="",bg="white",width=120)
        space_lbl3.pack()
        lbl_lst = []
        holder_msg = msg.msg
        if len(holder_msg) < 60:
            lbl = Label(actual_msg_frame,text=holder_msg,font=("Arial",12),bg="white")
            lbl.pack(side=TOP,anchor=W,pady=5)
        while len(holder_msg) >60:
            if(len(holder_msg[60:])>60):
                tmp_msg = holder_msg[:60]+" -"
            else:
                tmp_msg = holder_msg[:60]
            lbl_lst.append(Label(actual_msg_frame,text=tmp_msg,font=("Arial",12),bg="white"))
            holder_msg = holder_msg[60:]
        
        for lbl in lbl_lst:
            lbl.pack(side=TOP,anchor=W,pady=5)

        if msg.img_name!="no":
            try:
                print(msg.img_name)
                print("yop")
                self.expand_msg_img_lst.append(ImageTk.PhotoImage(Image.open(f"pictures\\{msg.img_name}")))
                img_lbl = Label(actual_msg_frame,image=self.expand_msg_img_lst[self.expand_msg_ing_lst_index],bg="white")
                img_lbl.pack(side=TOP,anchor=W,pady=5)
                self.expand_msg_ing_lst_index+=1                 
            except:
                print("sup")
                space_lbl = Label(actual_msg_frame,height=4,text="",bg="white")
                space_lbl.pack(side=TOP,anchor=W,pady=5)
        else:
                space_lbl = Label(actual_msg_frame,height=4,text="",bg="white")
                space_lbl.pack(side=TOP,anchor=W,pady=5) 

        actual_msg_frame.pack(side=TOP,pady=10)   

        comment_lbl = Label(msg_frame,text="Comments:",font=("Arial",15,font.BOLD),bg="white")
        comment_lbl.pack(side=TOP,anchor=W)       


        lst_to_pack = [msg_frame] + comments_frame_lst
        for frame in lst_to_pack:
            frame.pack(fill=X,pady=10,expand=TRUE)

        scroll_bar.pack(side=RIGHT,fill=Y)
        canvas.pack(fill=BOTH,expand=TRUE)
        main_frame.pack(fill=BOTH,expand=TRUE)

   
    def on_mousewheel(self,event,canvas):
        canvas.yview_scroll(-1*(event.delta//120), "units")

    def create_chatroom(self):
        toplevel = Toplevel(bg="white")
        toplevel.grab_set()
        toplevel.geometry("450x300")
        title_frame = Frame(toplevel,bg="#6666ff")
        title_msg_lbl = Label(title_frame,bg="#6666ff",fg="white",text="Create New Room",font=("Arial",20,font.BOLD))
        title_msg_lbl.pack(padx=50)
        title_frame.pack(fill=X,side=TOP)

        name_frame = Frame(toplevel,bg="white")
        chat_name_lbl = Label(name_frame,text="Room Name:",bg="white",font=("Arial",15))
        chat_name_entry = Entry(name_frame,highlightbackground="#0066ff", highlightthickness=2)
        chat_name_lbl.pack(side=LEFT,padx=10)
        chat_name_entry.pack(side=LEFT,padx=10)
        name_frame.pack(side=TOP,pady=10,anchor=W,padx=10)


        msg_lbl = Label(toplevel,text="When inputting topics and banned words, make sure to sepeate them by a ','")

        topics_frame = Frame(toplevel,bg="white")
        topics_lbl = Label(topics_frame,text="Room Topics:",bg="white",font=("Arial",15))
        topics_entry = Entry(topics_frame,width=40,highlightbackground="#0066ff", highlightthickness=2)
        topics_msg = Label(topics_frame,text="Separate the topics with ','",font=("Arial",10),bg="white")
        topics_lbl.grid(column=0,row=0,padx=15)
        topics_entry.grid(column=1,row=0)
        topics_msg.grid(column=1,row=1)
        topics_frame.pack(side=TOP,pady=10,anchor=W)
        
        banned_frame = Frame(toplevel,bg="white")
        banned_words_lbl = Label(banned_frame,text="Banned Words:",bg="white",font=("Arial",15))
        banned_words_entry = Entry(banned_frame,width=40,highlightbackground="#0066ff", highlightthickness=2)
        banned_words_msg = Label(banned_frame,text="Separate the words with ','",font=("Arial",10),bg="white")
        banned_words_lbl.grid(column=0,row=0,padx=10)
        banned_words_entry.grid(column=1,row=0)
        banned_words_msg.grid(column=1,row=1)
        banned_frame.pack(side=TOP,pady=10,anchor=W)

        

        create_btn = Button(toplevel,text="Create Room!",bg = "white",font=("Arial",15), command=lambda:self.mange_creating_new_room(chat_name_entry.get(),topics_entry.get(),banned_words_entry.get(),toplevel))
        create_btn.pack(anchor=W,padx=20,pady=10)

    def mange_creating_new_room(self,name,topics,banned_words,toplevel):
        print(name)
        if self.user_controller.check_if_room_name_exists(name):
            messagebox.showerror(title="Room name already exists",message="Sorry but this room name is already in use")
        else:
            try:
                topics_lst = topics.split(",")
                banned_words_lst = banned_words.split(",")
            except:
                messagebox.showerror(title="wrong input",message="Sorry but your input of the fields was wrong, make sure to follow the rules stated")
                return
            result = self.user_controller.create_new_room_with_server(self.user,name,topics_lst,banned_words_lst)
            if result:
                toplevel.destroy()
            else:
                messagebox.showerror(title="Creating a room failed",message="The proccess you attempted has failed, try again")
    def make_frame_chat_list(self,lst,container_frame:Frame):
        result = []
        self.expand_img = ImageTk.PhotoImage(Image.open("program_pics\\maximize.png"))
        count =0
        for msg in lst:
            if count % 2 == 0:
                color ="#C8C8C8"
            else:
                color = "#F0F0F0"

            frame = Frame(container_frame,bg = color,highlightbackground="#0066ff", highlightthickness=2,width=300)
            time_lbl = Label(frame,text = msg.time_str,font=("Arial",12),bg = color)
            sent_in_btn = Button(frame,text = f"Room/{msg.sent_in.name}", font=("Arial",12,font.ITALIC,font.BOLD),borderwidth=0,bg = color,command=partial(self.manage_join_room_by_id,msg.sent_in.room_id))
            if(len(msg.title)>50):
                actual_title = msg.title[:50] + f"... By {msg.sent_by}"
            else:
                actual_title = msg.title + f" By {msg.sent_by}"
            title_lbl = Label(frame,text = actual_title,font=("arial",15,font.BOLD),bg = color)
            if(len(msg.msg)>50):
                actual_msg = msg.msg[:50] + "..."
            else:
                actual_msg = msg.msg
            msg_lbl = Label(frame,text = actual_msg,font=("Arial",12),bg = color,height=3)
            expand_btn = Button(frame,image=self.expand_img,command=partial(self.expand_message,msg),borderwidth=0,bg = color)

            space_lbl = Label(frame,text="",bg=color,width=100)
            space_lbl.pack()
            title_lbl.pack(side=TOP,anchor=W)
            time_lbl.pack(side=TOP,anchor=E,pady=5,padx=3) 
            sent_in_btn.pack(side=TOP,anchor=W,pady=5)
            msg_lbl.pack(pady=10,side=TOP,anchor=W)
            expand_btn.pack(side=BOTTOM,anchor=E,pady=5,padx=3)
        

            if msg.img_name!="":
                try:
                    self.chat_img_lst.append(ImageTk.PhotoImage(Image.open(f"pictures\\{msg.img_name}")))
                    img_lbl = Label(frame,image=self.chat_img_lst[self.chat_img_lst_index],bg = color)
                    img_lbl.pack(side=TOP,anchor=W)
                    self.chat_img_lst_index+=1                 
                except:
                    space_lbl = Label(frame,height=4,text="",bg=color)
                    space_lbl.pack(side=TOP,anchor=W)
            else:
                space_lbl = Label(frame,height=4,text="",bg=color)
                space_lbl.pack(side=TOP,anchor=W)
            count+=1
            result.append(frame)
        return result      
            
    '''
    main functions - 
    - main_menu_screen()
    - log_in_screen()
    - sign_up_screen()
    - in_chat_screen()
    - search_results()

    all other functions are supportive functions of these 5 main ones
    '''

    def in_chat_screen(self,chatroom:chatroom):
        try:
            self.refresh_btn.pack_forget()
        except:
            pass   
        self.current_chat_id = chatroom.room_id
        self.clear_screen()
        self.root.geometry("1150x800")
        self.root.configure(bg="white")
        top_frame = self.create_top_frame()
        top_frame.config(height=350)
        top_frame.pack(side=TOP,fill=X)

        info_frame = Frame(self.root,bg="#6666ff",width=600,borderwidth=0)
        room_name_lbl = Label(info_frame,bg="#6666ff",fg="white",text=chatroom.name,font=("Arial",20,font.BOLD))
        currently_connected_lbl = Label(info_frame,bg="#6666ff",fg="white",text=f"{chatroom.current_members} currently connected",font=("Arial",13))
        space_lbl = Label(info_frame,bg="#6666ff")
        #space_lbl.grid(column=0,row=0,padx=50)
        currently_connected_lbl.pack(side=RIGHT,anchor=S)
        room_name_lbl.pack(side=RIGHT,padx=250,pady=10)
        info_frame.pack(pady=20)



        #creating scrolling chat screen
        main_frame = Frame(self.root,bg="white",borderwidth=0)
        canvas = Canvas(main_frame,width="10",bg="white",borderwidth=0)
        scroll_bar = Scrollbar(main_frame,orient=VERTICAL,command=canvas.yview)
        canvas.configure(yscrollcommand=scroll_bar.set)
        canvas.bind("<Configure>",lambda event: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.bind_all("<MouseWheel>",lambda e:self.on_mousewheel(e,canvas))
        second_frame = Frame(canvas,bg="white",borderwidth=0)
        canvas.create_window((225,0),window=second_frame,anchor=NW)

        packing_frame = Frame(canvas,bg="white")
        user_stats_frame = self.user_stats(chatroom,packing_frame)
        user_stats_frame.pack(side=TOP,anchor=W,pady=5)
        back_to_feed_btn = Button(packing_frame,text="<< Back To Feed",bg="#6666ff",fg="white",font=("Arial",15),command=self.main_menu_screen)
        back_to_feed_btn.pack(side=BOTTOM,anchor=W,padx=10)
        packing_frame.pack(side=LEFT,anchor=N,pady=10,fill=Y)

        if not self.is_user_in_list(chatroom.members ):
            join_btn = Button(canvas,bg="#6666ff",fg="white",text="Join Room!",font=("Arial",15),command=lambda: self.manage_join_room(chatroom),borderwidth=0)
            join_btn.pack(side=RIGHT,anchor=N,pady=10,padx=20)

        self.add_msg_img = PhotoImage(file="program_pics\\add (1).png")
        add_btn = Button(canvas,image=self.add_msg_img,borderwidth=0,command=lambda:self.get_new_msg_info(chatroom),bg="white")
        add_btn.pack(side=BOTTOM,anchor=E)

        self.refresh_img = PhotoImage(file="program_pics\\circular-left-arrow (1).png")
        self.refresh_btn = Button(canvas,image=self.refresh_img,borderwidth=0,command=lambda:self.manage_join_room_by_id(self.current_chat_id),bg="white")      



        frame_lst = self.make_frame_chat_list(chatroom.msgs,second_frame)
        for frame in frame_lst:
            frame.pack(fill=BOTH,pady=10,expand=TRUE)

        scroll_bar.pack(side=RIGHT,fill=Y)
        canvas.pack(fill=BOTH,expand=TRUE)
        main_frame.pack(fill=BOTH,expand=TRUE)




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
        canvas.create_window((225,0),window=second_frame,anchor=NW)


        packing_frame = Frame(canvas)
        user_actions_frame = self.user_actions(packing_frame)
        user_actions_frame.pack(side=TOP,anchor=W,pady=5)
        packing_frame.pack(side=LEFT,anchor=N,pady=10)


        search_bar_frame = self.create_search_bar_frame(second_frame)
        search_bar_frame.pack(fill=X,pady=10,expand=TRUE)

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
        self.pic = PhotoImage(file='program_pics\\logo.png')
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
        self.pic = PhotoImage(file='program_pics\\logo.png')
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


    def search_keyword(self,keyword:str):
        self.clear_screen()
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
        canvas.create_window((225,0),window=second_frame,anchor=NW)


        result_dict = self.user_controller.send_and_recv_search_results(keyword)
        print(f"results dict {result_dict}")
        result_lst = []
        for key in result_dict:
            result_lst.append((key,result_dict[key]))
        frame_lst = self.make_frame_lst_of_chat_rooms(result_lst,second_frame)

        for frame in frame_lst:
            frame.pack(side=BOTTOM,fill=X,pady=10,expand=TRUE)

        scroll_bar.pack(side=RIGHT,fill=Y)
        canvas.pack(fill=BOTH,expand=TRUE)
        main_frame.pack(fill=BOTH,expand=TRUE)

    #log in/sign up function group

    def Do(self):
        pass

    def send_log_in_info(self):
        msg = self.user_controller.log_in(self.name_entry_log_in.get(),self.password_entry_log_in.get())
        print(msg)
        msg,user = msg[0],msg[1]
        if(msg == "no username"):
            messagebox.showerror(title="Log in failed",message="The username you enterd was inccorect, try again")     
        elif(msg=="password is inccorect"):
            messagebox.showerror(title="Log in failed",message="The password you enterd was inccorect, try again")        
        else:
            self.user = user
            self.main_menu_screen()

    def send_sign_up_info(self):
        if self.name_entry_sign_up.get()=="no":
            messagebox.showerror(title="Username is invalid",message="The username you tried to sign up with is not allowed")
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
    
    def user_actions(self,container_frame:Frame):
        frame = Frame(container_frame)
        msg_lbl = Label(frame,text="User Options:",font=("Arial",15,font.BOLD))
        change_password_btn = Button(frame,text="Change password",command=self.change_password_window,font=("Arial",13,font.ITALIC,font.BOLD,"underline"),borderwidth=0)
        join_room_by_id_btn = Button(frame,text="Join room by ID",command=self.join_room_by_id_window,font=("Arial",13,font.ITALIC,font.BOLD,"underline"),borderwidth=0)
        create_chat_room_btn = Button(frame,text="Create New Room",command=self.create_chatroom,font=("Arial",13,font.ITALIC,font.BOLD,"underline"),borderwidth=0)
        join_room_by_name_btn = Button(frame,text="Join room by name",command=self.join_room_by_name_window,font=("Arial",13,font.ITALIC,font.BOLD,"underline"),borderwidth=0)

        msg_lbl.pack(side=TOP)
        create_chat_room_btn.pack(side=TOP,pady=10)
        join_room_by_id_btn.pack(side=TOP,pady=10)
        join_room_by_name_btn.pack(side=TOP,pady=10)
        change_password_btn.pack(side=TOP,pady=10)
        return frame

    def create_search_bar_frame(self,container_frame:Frame):
        frame = Frame(container_frame,highlightbackground="#0066ff", highlightthickness=2)

        search_bar_entry = Entry(frame,font=("Arial",15),highlightbackground="#0066ff", highlightthickness=2,width=50)

        search_btn = Button(frame,text="Search Room",font=("Arial",10,font.BOLD),highlightbackground="black", highlightthickness=2,bg="#0066ff",fg="white",command=lambda:self.check_search_phrase(search_bar_entry.get()))

        search_bar_entry.pack(side=LEFT,padx=10)
        search_btn.pack(side=LEFT,padx=10,pady=10)
        return frame
    
    def join_room_by_id_window(self):
        top_level = Toplevel(bg="white")
        top_level.attributes('-topmost', True)
        msg_lbl = Label(top_level,text="Join Room by ID",bg="#6666ff",fg="white",font=("Arial",15))
        id_entry = Entry(top_level,width=20,highlightbackground="#0066ff", highlightthickness=2)
        submit_btn = Button(top_level,text="Join!",bg="white",command=lambda:self.manage_join_room_by_id(id_entry.get(),top_level))
        msg_lbl.pack(padx=20,pady=10,fill=X)
        id_entry.pack()
        submit_btn.pack(pady=10)
    
    def join_room_by_name_window(self):
        top_level = Toplevel(bg="white")
        top_level.attributes('-topmost', True)
        msg_lbl = Label(top_level,text="Join Room by name",bg="#6666ff",fg="white",font=("Arial",15))
        name_entry = Entry(top_level,width=20,highlightbackground="#0066ff", highlightthickness=2)
        submit_btn = Button(top_level,text="Join!",bg="white",command=lambda:self.manage_join_room_by_name(name_entry.get(),top_level))
        msg_lbl.pack(padx=20,pady=10,fill=X)
        name_entry.pack()
        submit_btn.pack(pady=10)       
    
    def manage_join_room_by_id(self,id_num,*top_level):
        try:
            tmp = int(id_num)
        except:
            messagebox.showerror(title = "wrong ID",message="ID has to be a postibe number")
            return

        chat_room = self.user_controller.get_room_by_id(id_num,self.user.name)

        if not isinstance(chat_room,chatroom):
            if isinstance(chat_room,bool):
                messagebox.showerror(title="Room not found",message="The room you tried to reach wasn't found")
            else:
                messagebox.showerror(title="ID not found",message="the ID you entered had no matching results")
        else:
            self.in_chat_screen(chat_room)
            try:
                top_level[0].destroy()
            except IndexError:
                pass
    
    def manage_join_room_by_name(self,name,*top_level):
        if name == "":
            messagebox.showerror(title = "bad name",message="name can not be blank")
            return

        chat_room = self.user_controller.get_room_by_name(self.user.name,name)

        if not isinstance(chat_room,chatroom):
            if isinstance(chat_room,bool):
                messagebox.showerror(title="Room not found",message="The room you tried to reach wasn't found")
            else:
                messagebox.showerror(title="ID not found",message="the ID you entered had no matching results")
        else:
            self.in_chat_screen(chat_room)
            try:
                top_level[0].destroy()
            except IndexError:
                pass
    
    def change_password_window(self):
        top_level = Toplevel(bg="white")
        top_level.attributes('-topmost', True)
        msg_lbl = Label(top_level,text="Change Password",bg="#6666ff",fg="white",font=("Arial",15))
        new_pass_entry = Entry(top_level,width=20,highlightbackground="#0066ff", highlightthickness=2)
        submit_btn = Button(top_level,text="Join!",bg="white",command=lambda:self.manage_change_password(new_pass_entry.get(),top_level))
        msg_lbl.pack(padx=20,pady=10,fill=X)
        new_pass_entry.pack()
        submit_btn.pack(pady=10)
    
    def manage_change_password(self,new_pass,*top_level):
        if new_pass == "":
            messagebox.showerror(title="invalid password",message="password can not be blank")
            try:
                top_level[0].destroy()
                return
            except IndexError:
                return
        result = self.user_controller.change_password(self.user,new_pass)
        if result:
            messagebox.showinfo(title="Password changed",message="Password changed successfully")
            try:
                top_level[0].destroy()
                return
            except IndexError:
                return
        else:
            messagebox.showerror(title="Password was not changed",message="The procces was unsuccessful")
            try:
                top_level[0].destroy()
                return
            except IndexError:
                return        
            

    #in chat screen function group
    def user_stats(self,chatroom,containter_frame:Frame):
        frame = Frame(containter_frame,bg="white")
        msg_lbl = Label(frame,text="Room Info:",font=("Arial",15),bg="white")
        created_by_lbl = Label(frame,text=f"Created by {chatroom.creator.name}",font=("Arial",15),bg="white")
        members_lbl = Label(frame,text=f"This room has {len(chatroom.members)} members",font=("Arial",15),bg="white")
        msg_lbl.pack(side=TOP,pady=10,anchor=W)
        created_by_lbl.pack(side=TOP,pady=10,anchor=W)
        members_lbl.pack(side=TOP,pady=10,anchor=W)

        return frame
    
    def get_new_msg_info(self,chat_room:chatroom):
        print('yo')
        if self.user_controller.refresh:
            messagebox.showerror(title="can not add a message",message="you need to refresh before adding another message")
            return
        top_level = Toplevel()
        top_level.attributes('-topmost', True)
        self.filename = ""
        title_lbl = Label(top_level,text="Enter the title of your post:")
        title_entry = Entry(top_level)

        msg_lbl = Label(top_level,text="Enter the text of your post:")
        msg_entry = Entry(top_level,width=70)
        print("yoyo?")
        add_img_btn = Button(top_level,text="Add Image",command=self.select_img_for_message)

        create_btn = Button(top_level,text="Create!",command=lambda :self.check_new_msg_fields(self.user.name,msg_entry.get(),
        chat_room,self.filename,title_entry.get(),top_level))

        title_lbl.grid(row=0,column=0,pady=10)
        title_entry.grid(row=0,column=1,pady=10)
        msg_lbl.grid(row=1,column=0,pady=10)
        msg_entry.grid(row=1,column=1,pady=10)
        create_btn.grid(row=2,column=0,pady=10)
        add_img_btn.grid(row=2,column=1,pady=10)


    def select_img_for_message(self):
        self.filename = filedialog.askopenfilename(filetypes=[('image files', '.png'), ('image files', '.jpg')], )

    def check_new_msg_fields(self,name,msg,chat_room,img_name,title,top_level):
        img_and_path = img_name
        img_name = img_name[img_name.rfind("/")+1:]
        if img_name.count(".") > 1:
            messagebox.showerror(title="problem with the image",message="the image you selected has a dot in its name which is not allowed")
            return
        try:
            width,height = Image.open(img_and_path).size
            if width > 300:
                messagebox.showerror(title="image's width is too big",message="Sorry but this application does not suport images with a width above 250 px")
                return
            if height > 300:
                messagebox.showerror(title="image's height is too big",message="Sorry but this application does not suport images with a height above 300 px")
                return
        except AttributeError:
            pass
        if len(title) > 60:
            messagebox.showerror(title="title is too long",message="the title is not allowed to be over 60 chars")
            return
        self.user_controller.create_message_and_sent_to_server(name,msg,chat_room,img_and_path,title)
        top_level.destroy()

    def manage_join_room(self,chat_room:chatroom):
        result = self.user_controller.join_room(self.user,chat_room)
        if isinstance(result,str):
            messagebox.showerror(title="room not found",message="The room you tried to reach has expired")
        elif result:
            messagebox.showinfo(title="joined room",message=f"You have joined {chat_room.name}!")
        else:
            messagebox.showerror(title="joinning room failed",message="The procces failed, you did not join this room")

    def is_user_in_list(self,members:list[User]) ->bool:
        for member in members:
            if member.name == self.user.name:
                return True
        return False
    #search results function group

    def check_search_phrase(self,phrase:str):
        if phrase == "":
            messagebox.showerror(title="blank search",message="You have to input a keyword to search for")
            return
        if phrase.count(" ") > 0:
            messagebox.showerror(title="can not search for a phrase",message="You were trying to search for a phrase,unfortunately you can only search a keyword")
            return
        self.search_keyword(phrase)

    def make_frame_lst_of_chat_rooms(self,lst:list[(chatroom,int)],container_frame:Frame):
        result = []
        count=0
        for chat_room,score in lst:
            if count % 2 == 0:
                color ="#C8C8C8"
            else:
                color = "#F0F0F0"

            frame = Frame(container_frame,bg = color,highlightbackground="#0066ff", highlightthickness=2,width=300)
            
            room_btn = Button(frame,text=f"Room/{chat_room.name}",font=("Arial",15),bg=color,command=partial(self.manage_join_room_by_id,chat_room.room_id))
            members_joined_lbl = Label(frame,text = f"{len(chat_room.members)} members",font=("Arial",15),bg=color)
            score_lbl = Label(frame,text=f"{score}% match",font=("Arial",15),bg=color)
            go_to_room_btn = Button(frame,text="go to room",font=("Arial",15),bg=color,command=partial(self.manage_join_room_by_id,chat_room.room_id))

            room_btn.grid(row=0,column=0,pady=10,padx=20)
            members_joined_lbl.grid(row=1,column=0,pady=10)
            score_lbl.grid(row=0,column=1,pady=10,padx=20)
            go_to_room_btn.grid(row=2,column=1,pady=10,padx=20)
            count+=1

            result.append(frame)
        return result

rot = Tk()

ui = ui_reddit(rot)

ui.log_in_screen()
_thread.start_new_thread(ui.refresh_chat_room,())


rot.mainloop()
