import tkinter as tk
from windows.measuring_device_window import MeasuringDeviceWindow
from windows.automation_device_window import AutomationDeviceWindow
from windows.weather_data_window import WeatherDataWindow
from windows.email_window import EmailWindow

class MainWindow(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.configure(bg="lightblue")

        self.label = tk.Label(self, text="Welcome to OpenWeatherAutoHub", font=("Arial", 24), bg="lightblue")
        self.label.pack(pady=50)

        button_frame = tk.Frame(self, bg="lightblue")
        button_frame.pack(pady=20)

        self.measuring_device_window_button = tk.Button(
            button_frame, text="Measuring Devices", font=("Arial", 14),
            command=lambda: self.master.switch_frame(MeasuringDeviceWindow)
        )
        self.measuring_device_window_button.pack(side="left", padx=10, pady=10)

        self.automation_device_window_button = tk.Button(
            button_frame, text="Automation Devices", font=("Arial", 14),
            command=lambda: self.master.switch_frame(AutomationDeviceWindow)
        )
        self.automation_device_window_button.pack(side="left", padx=10, pady=10)

        self.weather_data_window_button = tk.Button(
            button_frame, text="Weather data", font=("Arial", 14),
            command=lambda: self.master.switch_frame(WeatherDataWindow)
        )
        self.weather_data_window_button.pack(side="left", padx=10, pady=10)

        self.mail_window_button = tk.Button(
            button_frame, text="Email window", font=("Arial", 14),
            command=lambda: self.master.switch_frame(EmailWindow)
        )
        self.mail_window_button.pack(side="left", padx=10, pady=10)
