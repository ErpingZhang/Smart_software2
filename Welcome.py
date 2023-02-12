from Detect import *


class Welcome_win:
    def __init__(self, win, title, size):
        self.win = win
        self.title = title
        self.size = size
        self.user_input = tk.Entry(self.win, width=35)
        self.pass_input = tk.Entry(self.win, width=35)

    def Tech(self):       # functions used to create the Technical support window
        tech = tk.Toplevel(self.win)
        tech.title("Technical Support")
        tech.geometry("450x300")
        Edward_text = tk.Label(tech, text="Edward He              hey113@mcmaster.ca", font=("Arial", 14))
        Erping_text = tk.Label(tech, text="Erping Zhang          zhange19@mcmaster.ca", font=("Arial", 14))
        Guangwei_text = tk.Label(tech, text="Guangwei Tang      tangg5@mcmaster.ca", font=("Arial", 14))
        Peihua_text = tk.Label(tech, text="Peihua Jin               jinp@mcmaster.ca", font=("Arial", 14))
        Peng_text = tk.Label(tech, text="Peng Cui                cuip1@mcmaster.ca", font=("Arial", 14))

        Edward_text.place(x=40, y=40)
        Erping_text.place(x=40, y=70)
        Guangwei_text.place(x=40, y=100)
        Peihua_text.place(x=40, y=130)
        Peng_text.place(x=40, y=160)

    def Input(self):      # functions used to take the input from the computer
        user = self.user_input.get()
        password = self.pass_input.get()
        if (user == "user001") and (password == "123456"):
            self.win.destroy()
            det_win = tk.Tk()
            detect_window = Det_Window(det_win)
            detect_window.content()
        else:
            entry_error = tk.Label(self.win, text="The username or password entered is wrong", fg='red')
            entry_error.place(x=70, y=190)

    def content(self):
        self.win.geometry(self.size)
        self.win.title(self.title)
        user_text = tk.Label(self.win, text="Username -")
        user_text.place(x=70, y=90)

        self.user_input.place(x=150, y=90, width=200)

        pass_text = tk.Label(self.win, text="Password -")
        pass_text.place(x=70, y=150)

        self.pass_input.place(x=150, y=150, width=200)

        login = tk.Button(self.win, text="Login",
                          bg='yellow', command=self.Input)
        login.place(x=190, y=225, width=70)

        tech_su = tk.Button(self.win, text="Tech Support",
                            bg='yellow', command=self.Tech)
        tech_su.place(x=325, y=250, width=100)

        self.win.mainloop()
