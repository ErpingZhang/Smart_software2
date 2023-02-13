from Welcome import *
import tkinter as tk
from diff import *
path = r"C:\Users\tgw19\Desktop\test"
createFolder(path)

wel_win = tk.Tk()
welcome_window = Welcome_win(wel_win, "Login Page", "450x300")
welcome_window.content()
