from Search import *
import tkinter as tk
from human_tracking import *
from diff import *


class Det_Window:
    def __init__(self, window):
        self.window = window
        self.variable = tk.StringVar(self.window)
        self.label = Label()
        self.choose_list = ["1 Day", "7 Days", "30 Days", "100 Days", "365 Days"]

    def content(self):
        self.window.title("Detect Window")
        self.window.geometry("1500x800")
        search_begin = tk.Label(self.window, text="Want to search an object?\n\n Choose time interval\n and start to search !!!", font=("Arial", 14))
        search_begin.place(x=1200, y=200)    # creating the choose button for date interval search
        self.variable.set("Choose a date")
        w = tk.OptionMenu(self.window, self.variable, *self.choose_list)
        w.pack()
        w.place(x=1250, y=300)
        ob_search = tk.Button(self.window, text="Search !",
                          bg='yellow', command=self.search)
        ob_search.place(x=1275, y=350, width=70)

        self.window.mainloop()

    def search(self):
        inp = self.variable.get().split(" ")[0]
        search_window = Sear_Window(self.window, 0-int(inp))
        search_window.sea()



