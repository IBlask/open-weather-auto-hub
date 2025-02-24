import tkinter as tk
from tkinter import ttk, messagebox, Canvas, Frame
import requests
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

API_URL_WEATHER = "http://127.0.0.1:5000/api/weather-data"

class WeatherDataWindow(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.configure(bg="lightblue")

        header_frame = tk.Frame(self, bg="lightblue")
        header_frame.pack(fill="x", padx=10, pady=10)

        self.label = tk.Label(header_frame, text="Weather Data", font=("Arial", 20), bg="lightblue")
        self.label.pack(side="left", expand=True, anchor="center")

        self.type_entry = self.create_labeled_dropdown("Type:", ["All", "temperature", "humidity", "pressure", "wind"])
        self.device_entry = self.create_labeled_entry("Device Public Key:")
        self.start_entry = self.create_labeled_entry("Start Time (YYYY-mm-dd_HH:MM:SS):")
        self.end_entry = self.create_labeled_entry("End Time (YYYY-mm-dd_HH:MM:SS):")
        self.last_n_entry = self.create_labeled_entry("Last N Records:")

        self.fetch_button = tk.Button(self, text="Fetch Weather Data", command=self.fetch_weather_data)
        self.fetch_button.pack(pady=10)

        self.graph_frame = tk.Frame(self, bg="lightblue")
        self.graph_frame.pack(fill="both", expand=True, pady=10)

        self.back_button = tk.Button(self, text="Back to Main Window", command=self.switch_back)
        self.back_button.pack(side="bottom", pady="10")


    def create_labeled_entry(self, label_text):
        frame = tk.Frame(self, bg="lightblue")
        frame.pack(pady=5)
        label = tk.Label(frame, text=label_text, font=("Arial", 12), bg="lightblue")
        label.pack(side="left", padx=5)
        entry = tk.Entry(frame, font=("Arial", 12))
        entry.pack(side="left", padx=5)
        return entry

    def create_labeled_dropdown(self, label_text, options):
        frame = tk.Frame(self, bg="lightblue")
        frame.pack(pady=5)
        label = tk.Label(frame, text=label_text, font=("Arial", 12), bg="lightblue")
        label.pack(side="left", padx=5)
        var = tk.StringVar(value=options[0])
        dropdown = ttk.Combobox(frame, textvariable=var, values=options, font=("Arial", 12), state="readonly")
        dropdown.pack(side="left", padx=5)
        return dropdown

    def fetch_weather_data(self):
        params = {
            "type": self.type_entry.get(),
            "measuring_device": self.device_entry.get(),
            "start_time": self.start_entry.get(),
            "end_time": self.end_entry.get(),
            "last_n": self.last_n_entry.get(),
        }

        params = {k: v for k, v in params.items() if v and v != "All"}

        try:
            response = requests.get(API_URL_WEATHER, params=params)
            response.raise_for_status()

            data = response.json()

            if isinstance(data, dict) and "message" in data:
                messagebox.showerror("Error", data["message"])
            else:
                self.display_weather_graph(data)
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"Failed to retrieve weather data: {e}")

    def display_weather_graph(self, data):
        for widget in self.graph_frame.winfo_children():
            widget.destroy()

        data_types = list(data.keys())
        num_graphs = len(data_types)

        if num_graphs == 0:
            messagebox.showinfo("Info", "No weather data found.")
            return

        fig_size = (5, 3) if num_graphs == 1 else (8, 5)

        if num_graphs == 1:
            fig, ax = plt.subplots(figsize=fig_size)
            axes = [ax]
        else:
            nrows = 2
            ncols = 2
            fig, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=fig_size)
            axes = axes.flatten()

        for i, ax in enumerate(axes[:num_graphs]):
            data_type = data_types[i]
            records = data[data_type]

            timestamps = [record.get("measured_at", "N/A") for record in records]
            values = [record.get("value", record.get("speed", "N/A")) for record in records]

            ax.plot(timestamps, values, marker="o", linestyle="-", label=data_type)
            ax.set_title(f"{data_type.capitalize()} Over Time", fontsize=9)
            ax.set_xlabel("Time", fontsize=7)
            ax.set_ylabel(f"{data_type.capitalize()}", fontsize=7)
            ax.legend(fontsize=7)

            if len(timestamps) > 1:
                ax.set_xticks([0, len(timestamps) - 1])
                ax.set_xticklabels([timestamps[0], timestamps[-1]], fontsize=7, rotation=0)
            else:
                ax.set_xticks([0])
                ax.set_xticklabels([timestamps[0]], fontsize=7, rotation=0)

            ax.margins(x=0.1)

        plt.subplots_adjust(hspace=0.3, wspace=0.3)
        plt.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
        canvas.draw()
        widget = canvas.get_tk_widget()
        
        widget.pack(expand=True, anchor="center", pady=10)


    def switch_back(self):
        from windows.main_window import MainWindow
        self.master.switch_frame(MainWindow)
