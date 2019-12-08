import tkinter as tk


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.geometry("600x600")
        # self.master.resizable(0, 0)
        self.pack()
        self.create_widgets()
        self.number = 0

    def create_widgets(self):
        self.winfo_toplevel().title("Doge Explorer")
        self.hi_there = tk.Button(self)
        self.hi_there["text"] = 0
        self.hi_there["command"] = self.say_hi
        self.hi_there.pack(side="top")

        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=self.master.destroy)
        self.quit.pack(side="bottom")

    def say_hi(self):
        self.hi_there["text"] = self.number
        self.number = self.number + 1


root = tk.Tk()
app = Application(master=root)
app.mainloop()
