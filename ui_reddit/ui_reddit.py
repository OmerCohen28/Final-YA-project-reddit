from tkinter import *

#To Do - display Images in chatroom!!!

class ui_reddit:

    def __init__(self,root:Tk) ->None:
        self.root = root

    #clear the screen
    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()


    #screen that shows chat_rooms you've joined, if you haven't joined any it'll suggest you to join some
    #also shows some user and social info, have to think what
    def main_menu_screen(self):
        pass

    #log-in screen for poeple to sign in/log-in as guests
    def log_in_screen(self):
        pass

    #shows the listbox of the chat + some other fetures
    #make it an option to click on a certain message and comment on it
    def in_chat_screen(self):
        pass

    #screen after clicking on a message, maybe open a whole new screen or maybe change the current one
    #shows comments on a message
    def comment_section_screen(self):
        pass 