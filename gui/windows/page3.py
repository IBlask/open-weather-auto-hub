import tkinter as tk

class Page3(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.configure(bg="lightgreen")

        self.label = tk.Label(self, text="This is Page 3", font=("Arial", 24))
        self.label.pack(pady=50)
