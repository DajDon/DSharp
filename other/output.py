from tkinter import Tk, Button, Label, Entry

root = Tk()
root.title("Name Entry")
root.geometry("400x150")

lbl = Label(root, text="Your name:")
lbl.place(x=20, y=20)

name_box = Entry(root)
name_box.place(x=20, y=50)

def btn_click():
    name_box.delete(0, "end")
    name_box.insert(0, "Hello " + name_box.get())

btn = Button(root, text="Greet", command=btn_click)
btn.place(x=20, y=80)

root.mainloop()
