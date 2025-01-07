import tkinter as tk

class Page2(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.configure(bg="lightgreen")

        self.label = tk.Label(self, text="This is Page 2", font=("Arial", 24))
        self.label.pack(pady=50)

        self.button = tk.Button(self, text="Back to Main Window", command=self.switch_back)
        self.button.pack(pady=20)

    def switch_back(self):
        from windows.main_window import MainWindow
        self.master.switch_frame(MainWindow)
