import customtkinter as ctk
from tkinter import filedialog
import requests
import threading
import os, sys
from PIL import Image, ImageTk

root = ctk.CTk()
root.title("D# Settings")
root.geometry("350x500")
root.resizable(False, False)
root.config(bg="#181818")

icon_path = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "assets", "logo.ico"
)
root.iconbitmap(icon_path) 

def saveApiKey():
    with open("./api_key.txt", "w", encoding="utf-8") as f:
        f.write(apibox.get("1.0", "end"))

apibox = ctk.CTkTextbox(
    root,
    fg_color="#1e1b4b",
    text_color="white",
    border_color="white",
    border_width=2,
    width=300,
    height=25, 
    wrap="word"
)
apibox.place(relx=0.5, rely=0.14, anchor="center")


api_text = ctk.CTkLabel(
    root,
    text="Api Key",
    font=("Arial", 20),
    text_color="#ffffff",
    fg_color="#181818"
)
api_text.place(relx=0.18, rely=0.07, anchor="center")

save_button = ctk.CTkButton(
    root,
    text="Save",
    width=160,
    height=40,
    fg_color="#1e1b4b",
    text_color="white",
    corner_radius=8,
    hover_color="#262255",
    border_color="white",
    border_width=2,
    font=("Arial", 20),
    command=saveApiKey
)
save_button.place(relx=0.5, rely=0.9, anchor="center")



root.mainloop()