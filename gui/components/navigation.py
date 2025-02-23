import tkinter as tk
from windows.main_window import MainWindow
from windows.measuring_device_window import MeasuringDeviceWindow
from windows.automation_device_window import AutomationDeviceWindow
from windows.weather_data_window import WeatherDataWindow

class NavigationBar(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="blue")
        
        self.configure(width=parent.winfo_width(), height=50)

        button_frame = tk.Frame(self, bg="blue")
        button_frame.pack(side="left", fill="x", anchor="center")

        self.main_window_button = tk.Button(button_frame, text="Main Window", command=lambda: parent.switch_frame(MainWindow))
        self.main_window_button.pack(side="top", pady=10, padx=5, expand=False)

        self.measuring_device_window_button = tk.Button(button_frame, text="Measuring devices", command=lambda: parent.switch_frame(MeasuringDeviceWindow))
        self.measuring_device_window_button.pack(side="top", pady=10, padx=5, expand=False)

        self.automation_device_window_button = tk.Button(button_frame, text="Automation devices", command=lambda: parent.switch_frame(AutomationDeviceWindow))
        self.automation_device_window_button.pack(side="top", pady=10, padx=5, expand=False)

        self.weather_data_window_button = tk.Button(button_frame, text="Weather data", command=lambda: parent.switch_frame(WeatherDataWindow))
        self.weather_data_window_button.pack(side="top", pady=10, padx=5, expand=False)