import tkinter as tk

class MainWindow(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.configure(bg="lightblue")

        self.label = tk.Label(self, text="Welcome to OpenWeatherAutoHub", font=("Arial", 24))
        self.label.pack(pady=50)

        self.button = tk.Button(self, text="Measuring devices", command=self.switch_page)
        self.button.pack(pady=20)

    def switch_page(self):
        from windows.measuring_device_window import MeasuringDeviceWindow
        self.master.switch_frame(MeasuringDeviceWindow)
