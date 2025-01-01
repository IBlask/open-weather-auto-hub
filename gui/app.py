import tkinter as tk
from windows.main_window import MainWindow

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("OpenWeatherAutoHub GUI")
        self.geometry("1280x720")
        self.state("zoomed")
        self.current_frame = None
        self.switch_frame(MainWindow)

    def switch_frame(self, frame_class):
        if self.current_frame is not None:
            self.current_frame.destroy()
        self.current_frame = frame_class(self)
        self.current_frame.pack(fill="both", expand=True)



if __name__ == "__main__":
    app = App()
    app.mainloop()
