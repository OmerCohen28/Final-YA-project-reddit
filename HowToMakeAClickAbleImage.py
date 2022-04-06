#Import all the necessary libraries
from tkinter import *
from PIL import ImageTk
from PIL import Image
#Define the tkinter instance
win= Tk()
win.title("Rounded Button")

#Define the size of the tkinter frame
win.geometry("700x800")

#Define the working of the button

def my_command():
   text.config(text= "You have clicked Me...")

#Import the image using PhotoImage function
click_btn= ImageTk.PhotoImage(Image.open("logo.png"))

#Let us create a label for button event
img_label= Label(image=click_btn)

#Let us create a dummy button and pass the image
button= Button(win, image=click_btn,command= my_command,
borderwidth=0)
button.pack(pady=30)

text= Label(win, text= "")
text.pack(pady=30)

win.mainloop()