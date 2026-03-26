from tkinter import Tk, Button, Label, Entry

root = Tk()
root.title("Calculator")
root.geometry("300x200")

title = Label(root, text="Enter numbers:")
title.place(x=20, y=20)

num1 = Entry(root)
num1.place(x=20, y=50)

num2 = Entry(root)
num2.place(x=20, y=80)

def calc_btn_click():
    a = int(num1.get())
    b = int(num2.get())
    print(a + b)

calc_btn = Button(root, text="Calculate", command=calc_btn_click)
calc_btn.place(x=20, y=110)

root.mainloop()