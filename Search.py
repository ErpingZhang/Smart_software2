from datetime import timedelta, date
from find import *
import os
import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk


class Sear_Window:
    def __init__(self, window, inpu):
        self.window = window
        self.sear = tk.Toplevel(window)
        self.Item_dir = "C:/Users/tgw19/Desktop/test/item"
        self.label = Label()
        self.image_sort = 0
        self.imge_list = []
        self.image_name = ""
        self.today = date.today()
        self.date_sub = inpu

    def sea(self):  # the first search window
        self.sear.title("Search Window")
        self.sear.geometry("800x500")
        self.sear.resizable(True, True)

        for images in os.listdir(self.Item_dir):
            # check if the image ends with png
            comp_date = self.today + timedelta(days=self.date_sub)
            print(images)
            image_name = os.path.splitext(self.Item_dir + "/" + images)
            print(image_name)
            image_name = image_name[0].split("/")[len(image_name[0].split("/"))-1]
            print(image_name)
            image_name = image_name.split("_")
            print(image_name)
            image_date = date(int(image_name[1]), int(image_name[2]), int(image_name[3]))
            if image_date >= comp_date:
                self.imge_list.append(images)
        self.image_name = os.path.splitext(self.Item_dir + "/" + self.imge_list[0])
        self.image_name = self.image_name[0].split("/")[len(self.image_name[0].split("/"))-1]
        self.image_name = self.image_name.split("_")[0]
        ima = Image.open(self.Item_dir + "/" + self.imge_list[0])
        img = ImageTk.PhotoImage(ima)
        # Create a Label Widget to display the text or Image
        self.label = Label(self.sear, image=img)
        self.label.window = self.sear
        self.label.image = img
        self.label.pack()
        self.label.place(x=75, y=100)
        next_img = tk.Button(self.sear, text="Next", bg='yellow', command=self.nex_img)
        next_img.place(x=300, y=400, width=70)
        prev_img = tk.Button(self.sear, text="Previous", bg='yellow', command=self.pre_img)
        prev_img.place(x=100, y=400, width=70)
        find = tk.Button(self.sear, text="Find it", bg='yellow', command=self.find_img)
        find.place(x=600, y=200, width=70)

    def nex_img(self):
        self.label.config(image='')
        if self.image_sort == len(self.imge_list) - 1:
            self.image_sort = 0
        else:
            self.image_sort += 1
        self.image_name = os.path.splitext(self.Item_dir + "/" + self.imge_list[self.image_sort])
        self.image_name = self.image_name[0].split("/")[len(self.image_name[0].split("/"))-1]
        self.image_name = self.image_name.split("_")[0]
        ima = Image.open(self.Item_dir + "/" + self.imge_list[self.image_sort])
        img = ImageTk.PhotoImage(ima)
        # Create a Label Widget to display the text or Image
        self.label = Label(self.sear, image=img)
        self.label.window = self.sear
        self.label.image = img
        self.label.pack()
        self.label.place(x=75, y=100)

    def pre_img(self):
        self.label.config(image='')
        if self.image_sort == 0:
            self.image_sort = len(self.imge_list) - 1
        else:
            self.image_sort -= 1
        self.image_name = os.path.splitext(self.Item_dir + "/" + self.imge_list[self.image_sort])
        self.image_name = self.image_name[0].split("/")[len(self.image_name[0].split("/"))-1]
        self.image_name = self.image_name.split("_")[0]
        ima = Image.open(self.Item_dir + "/" + self.imge_list[self.image_sort])
        img = ImageTk.PhotoImage(ima)
        # Create a Label Widget to display the text or Image
        self.label = Label(self.sear, image=img)
        self.label.window = self.sear
        self.label.image = img
        self.label.pack()
        self.label.place(x=75, y=100)

    def find_img(self):
        self.sear.destroy()
        fin_window = Find_Window(self.window, self.image_name)
        fin_window.fin()
