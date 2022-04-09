import tkinter as tk
import glob
 
 
root = tk.Tk()
root.geometry("400x400")
def showimg(e):
	n = lst.curselection()
	fname = lst.get(n)
	img = tk.PhotoImage(file=fname)
	lab.config(image=img)
	lab.image = img
	print(fname)
 
lst = tk.Listbox(root)
lst.pack(side="left", fill=tk.Y, expand=1)
namelist = [i for i in glob.glob("*png")]
for fname in namelist:
	lst.insert(tk.END, fname)
lst.bind("<<ListboxSelect>>", showimg)
img = tk.PhotoImage(file="Idle (5)_ltl.png")
lab = tk.Label(root, text="hello", image=img)
lab.pack(side="left")
 
root.mainloop()