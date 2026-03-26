import tkinterweb
from tkinterweb import HtmlFrame
from tkinter import *
import customtkinter as ctk
import sys

root = ctk.CTk()
root.resizable(False, False)
root.title("D# Wiki")
root.geometry("1200x700")

from PIL import Image, ImageTk
root.iconbitmap("assets/logo.ico")

img = ImageTk.PhotoImage(Image.open("assets/logo.png"))
root.iconphoto(True, img)   

website = HtmlFrame(root, messages_enabled=True) 
website.load_website("https://dajdon.hu/dsharp/wiki.html") 
website.pack(fill="both", expand=True) 

root.mainloop()