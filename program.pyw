import customtkinter as ctk
import customtkinter
import tkinter as tk
import requests
import threading
import os, sys
import ctypes
import webbrowser
from PIL import Image, ImageTk
import subprocess

root = ctk.CTk()
root.title("D# Programing")
root.geometry("1200x700")
root.resizable(False, False)
root.config(bg="#181818")

with open("api_key.dd", "r") as f:
    API_KEY = f.read().strip()
API_URL = "https://api.groq.com/openai/v1/chat/completions"

chat = [{"role": "system", "content": "You are a D# to Python 3 compiler. The user gives you D# v3.0 code and you return ONLY the Python 3 code. No explanation, no markdown, no extra text, no code blocks.\n\nD# v3.0 FULL TRANSPILATION RULES (INCLUDING GUI):\n\n--- LITERALS ---\nyes -> True\nno -> False\nempty -> None\n\n--- COMMENTS ---\nLines starting with // are comments. Remove them entirely.\n\n--- INPUT / OUTPUT ---\nshow(EXPR) -> print(EXPR)\nask(EXPR) -> input(EXPR)\n\n--- TYPE CONVERSIONS ---\ntext(X) -> str(X)\nnum(X) -> int(X)\ndecimal(X) -> float(X)\nsize(X) -> len(X)\n\n--- STRING METHODS ---\nX.up() -> X.upper()\nX.down() -> X.lower()\n\n--- VARIABLES & MATH ---\nNAME = EXPR -> NAME = EXPR\n+ - * / % ** (unchanged)\n== != > < >= <= (unchanged)\nand or not (unchanged)\n\n--- CONDITIONS ---\n'when COND =>'        -> 'if COND:'\n'or when COND =>'     -> 'elif COND:'\n'otherwise =>'        -> 'else:'\n\n--- LOOPS ---\n'repeat N =>'                     -> 'for _ in range(N):'\n'repeat i : A to B =>'            -> 'for i in range(A, B+1):'\n'repeat i : A to B by S =>'       -> 'for i in range(A, B+1, S):'\n'each item in LIST =>'            -> 'for item in LIST:'\n'whilst COND =>'                  -> 'while COND:'\n\n--- FUNCTIONS ---\n'func NAME(args) =>' -> 'def NAME(args):'\n'give back EXPR'     -> 'return EXPR'\n\n--- LISTS ---\nLIST << ELEM   -> LIST.append(ELEM)\nLIST >> ELEM   -> LIST.remove(ELEM)\nsize(LIST)     -> len(LIST)\n\n--- DICTIONARIES ---\n'drop DICT[KEY]' -> 'del DICT[KEY]'\nsize(DICT)       -> len(DICT)\n\n--- ERROR HANDLING ---\n'attempt =>'        -> 'try:'\n'c rescue =>'       -> 'except Exception:' (if user writes just rescue =>)\n'rescue =>'         -> 'except Exception:'\n'rescue as e =>'    -> 'except Exception as e:'\n\n--- GUI (tkinter) ---\nD# has a minimal GUI layer that maps to tkinter. Always assume tkinter is used.\n\nImports (add at top IF any GUI command appears anywhere in the code):\n- from tkinter import Tk, Button, Label, Entry\n\nWindow:\n- 'make window TITLE WIDTHxHEIGHT' ->\n    root = Tk()\n    root.title(TITLE)\n    root.geometry(\"WIDTHxHEIGHT\")\n\nWidgets:\n- 'add label NAME with TEXT at X, Y' ->\n    NAME = Label(root, text=TEXT)\n    NAME.place(x=X, y=Y)\n\n- 'add button NAME with TEXT at X, Y do =>' ->\n    def NAME_click():\n        ...block body...\n    NAME = Button(root, text=TEXT, command=NAME_click)\n    NAME.place(x=X, y=Y)\n\n- 'add entry NAME at X, Y' ->\n    NAME = Entry(root)\n    NAME.place(x=X, y=Y)\n\nEntry helpers:\n- 'read NAME'   -> 'NAME.get()'\n- 'write NAME with TEXT' -> in Python: 'NAME.delete(0, \"end\"); NAME.insert(0, TEXT)'\n\nMain loop:\n- 'start gui' -> 'root.mainloop()'\n\nExamples (GUI):\nD#:\n  make window \"Demo\" 400x200\n\n  add label title with \"Hello GUI\" at 20, 20\n\n  add entry name_box at 20, 60\n\n  add button go_btn with \"Greet\" at 20, 100 do =>\n      show(\"Hello \" + read name_box)\n\n  start gui\n\nPython:\n  from tkinter import Tk, Button, Label, Entry\n\n  root = Tk()\n  root.title(\"Demo\")\n  root.geometry(\"400x200\")\n\n  title = Label(root, text=\"Hello GUI\")\n  title.place(x=20, y=20)\n\n  name_box = Entry(root)\n  name_box.place(x=20, y=60)\n\n  def go_btn_click():\n      print(\"Hello \" + name_box.get())\n\n  go_btn = Button(root, text=\"Greet\", command=go_btn_click)\n  go_btn.place(x=20, y=100)\n\n  root.mainloop()\n\n--- INDENTATION ---\nPreserve the D# indentation. Every line ending with '=>' becomes a Python header line ending with ':' and increases indentation for the following block.\n\n--- OUTPUT RULES ---\n1) Output only valid Python 3 code.\n2) Do not output comments or explanations.\n3) Apply all substitutions (literals, functions, GUI, blocks) consistently.\n4) If a line has no D# keyword, output it unchanged as Python.\n"}]

root.iconbitmap("assets/logo.ico")

img = ImageTk.PhotoImage(Image.open("assets/logo.png"))
root.iconphoto(True, img)   

textbox = ctk.CTkTextbox(
    root,
    fg_color="#1e1b4b",
    text_color="white",
    border_color="white",
    border_width=2,
    width=1000,
    height=650, 
    wrap="word"
)
textbox.place(x=180, y=25)


def api(short_response=False):
    try:
        messages = chat.copy()
        if short_response:
            messages.append({"role": "system", "content": "Adj rövid, tömör választ (maximum 1 mondat)."})
        
        r = requests.post(
            API_URL,
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            json={"model": "llama-3.3-70b-versatile", "messages": messages}
        )
        ai = r.json()["choices"][0]["message"]["content"]
        chat.append({"role": "assistant", "content": ai})
        save_output(ai)
    except Exception as e:
        save_output(f"Error: {e}")

def send(short_response=False):
    msg = textbox.get("1.0", "end-1c")
    if not msg.strip():
        return
    chat.append({"role": "user", "content": msg})
    threading.Thread(target=lambda: api(short_response), daemon=True).start()

def start():
    subprocess.Popen(["python", "other/output.py"], creationflags=subprocess.CREATE_NEW_CONSOLE)

def save():
    with open("other/saved.ds", "w", encoding="utf-8-sig", newline="") as file:
        file.write(textbox.get("1.0", "end-1c"))

def open_file():
    with open("other/saved.ds", "r", encoding="utf-8-sig") as file:
        textbox.delete("1.0", "end")        
        textbox.insert("1.0", file.read()) 

def open_wiki_file():
    subprocess.Popen(["other/Wiki.exe"])

def save_output(msg):
    with open("other/output.py", "w", encoding="utf-8") as f:
        f.write(msg)

options_text = ctk.CTkLabel(
    root,
    text="Options",
    font=("Arial", 20),
    text_color="#ffffff",
    fg_color="#181818"
)
options_text.place(x=55, y=25)

compile_button = ctk.CTkButton(
    root,
    text="Compile",
    width=160,
    height=40,
    fg_color="#1e1b4b",
    text_color="white",
    corner_radius=8,
    hover_color="#262255",
    border_color="white",
    border_width=2,
    font=("Arial", 20),
    command=lambda: send(short_response=False)
)
compile_button.place(x=10, y=70) 

start_button = ctk.CTkButton(
    root,
    text="Start",
    width=160,
    height=40,
    fg_color="#1e1b4b",
    text_color="white",
    corner_radius=8,
    hover_color="#262255",
    border_color="white",
    border_width=2,
    font=("Arial", 20),
    command=start
)
start_button.place(x=10, y=125) 

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
    command=save
)
save_button.place(x=10, y=180) 

load1_button = ctk.CTkButton(
    root,
    text="Load",
    width=160,
    height=40,
    fg_color="#1e1b4b",
    text_color="white",
    corner_radius=8,
    hover_color="#262255",
    border_color="white",
    border_width=2,
    font=("Arial", 20),
    command=open_file
)
load1_button.place(x=10, y=235) 

help_button = ctk.CTkButton(
    root,
    text="Wiki",
    width=160,
    height=40,
    fg_color="#1e1b4b",
    text_color="white",
    corner_radius=8,
    hover_color="#262255",
    border_color="white",
    border_width=2,
    font=("Arial", 20),
    command=open_wiki_file
)
help_button.place(x=10, y=290) 

root.mainloop()