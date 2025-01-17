import tkinter as tk
from windows.main_window import MainWindow
from windows.page2 import Page2
from windows.page3 import Page3

class NavigationBar(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="blue")
        
        self.configure(width=parent.winfo_width(), height=50)

        button_frame = tk.Frame(self, bg="blue")
        button_frame.pack(side="left", fill="x", anchor="center")

        self.main_window_button = tk.Button(button_frame, text="Main Window", command=lambda: parent.switch_frame(MainWindow))
        self.main_window_button.pack(side="top", pady=10, padx=5, expand=False)

        self.page2_button = tk.Button(button_frame, text="Page 2", command=lambda: parent.switch_frame(Page2))
        self.page2_button.pack(side="top", pady=10, padx=5, expand=False)

        self.page3_button = tk.Button(button_frame, text="Page 3", command=lambda: parent.switch_frame(Page3))
        self.page3_button.pack(side="top", pady=10, padx=5, expand=False)

