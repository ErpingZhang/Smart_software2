import os
import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk


class Find_Window:
    def __init__(self, window, name):
        self.name = name
        self.find = tk.Toplevel(window)
        self.Location_dir = "C:/Users/13090/Desktop/testing/location"
        self.label = Label()
        self.image_sort = 0
        self.image_flag = 0
        self.image_name = ""

    def fin(self):
        self.find.title("Search Window")
        self.find.geometry("800x500")
        self.find.resizable(True, True)

        for images in os.listdir(self.Location_dir):
            # check if the image ends with png
            length = len(os.listdir(self.Location_dir))
            self.image_name = os.path.splitext(self.Location_dir + "/" + images)
            self.image_name = self.image_name[0].split("/")[len(self.image_name[0].split("/")) - 1]
            self.image_sort += 1
            if self.name == self.image_name:
                ima = Image.open(self.Location_dir + "/" + images)
                img = ImageTk.PhotoImage(ima)
                # Create a Label Widget to display the text or Image
                self.label = Label(self.find, image=img)
                self.label.window = self.find
                self.label.image = img
                self.label.pack()
                self.image_flag = 1
