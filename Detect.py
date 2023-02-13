from Search import *
import tkinter as tk
from human_tracking import *
from diff import *
import threading


class Det_Window:
    #---------------------------------Below is the human detection thread------------------------------#
    def __init__(self, window):
        self.window = window
        self.variable = tk.StringVar(self.window)
        self.label = Label()
        self.choose_list = ["1 Day", "7 Days", "30 Days", "100 Days", "365 Days"]

    def content(self):
        class HumanDetection(threading.Thread):  # 继承父类threading.Thread
            def __init__(self, threadID, name, counter):
                threading.Thread.__init__(self)
                self.threadID = threadID
                self.name = name
                self.counter = counter

            def run(self):  # 把要执行的代码写到run函数里面 线程在创建后会直接运行run函数
                
                tracking = human_tracking('com3',9600,1)
                path = r"C:\Users\tgw19\Desktop\test"
                while True:
                    human_tracking.begin_tracking(tracking, path)
                    key_pressed = cv2.waitKey(1) & 0xFF
                    if key_pressed == ord('q'):
                        break
        thread2 = HumanDetection(1, "detect", 1)
        thread2.start()

        # ----------------------------Below is the Detect Window part -------------------------------------------#
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



