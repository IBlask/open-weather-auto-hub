import tkinter as tk

class MainWindow(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.configure(bg="lightblue")

        self.label = tk.Label(self, text="Welcome to OpenWeatherAutoHub", font=("Arial", 24))
        self.label.pack(pady=50)

        self.button = tk.Button(self, text="Go to Page 2", command=self.switch_page)
        self.button.pack(pady=20)

    def switch_page(self):
        from windows.page2 import Page2
        self.master.switch_frame(Page2)
