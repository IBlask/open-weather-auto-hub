import tkinter as tk

import tkinter as tk
from tkinter import ttk, messagebox
import requests

API_URL_LIST = "http://127.0.0.1:5000/api/automation-device/list"
API_URL_ADD = "http://127.0.0.1:5000/api/automation-device"
API_URL_DELETE = "http://127.0.0.1:5000/api/automation-device" 

class AutomationDeviceWindow(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.configure(bg="lightgreen")

        self.label = tk.Label(self, text="Automation Devices", font=("Arial", 20), bg="lightgreen")
        self.label.pack(pady=10)

        table_frame = tk.Frame(self, bg="lightgreen")
        table_frame.pack(pady=10)

        columns = ("Name", "IP Address")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)
        self.tree.column("Name", width=350, anchor="center")  
        self.tree.column("IP Address", width=350, anchor="center")
        self.tree.heading("Name", text="Name")
        self.tree.heading("IP Address", text="IP Address")
        self.tree.pack(fill="both", padx=10, pady=1)

        self.device_data = {}

        button_frame = tk.Frame(self, bg="lightgreen")
        button_frame.pack(pady=10)

        self.fetch_button = tk.Button(button_frame, text="Fetch Devices", command=self.fetch_devices)
        self.fetch_button.pack(side="left", padx=5)

        self.delete_button = tk.Button(button_frame, text="Delete Selected Device", command=self.delete_device, bg="red", fg="white")
        self.delete_button.pack(side="left", padx=5)

        self.add_label = tk.Label(self, text="Add New Device", font=("Arial", 16), bg="lightgreen")
        self.add_label.pack(pady=10)

        self.name_entry = self.create_labeled_entry("Device Name:")
        self.ip_entry = self.create_labeled_entry("Device IP Address:")

        self.add_button = tk.Button(self, text="Add Device", command=self.add_device)
        self.add_button.pack(pady=10)

        self.back_button = tk.Button(self, text="Back to Main Window", command=self.switch_back)
        self.back_button.pack(pady=50)

    def create_labeled_entry(self, label_text):
        frame = tk.Frame(self, bg="lightgreen")
        frame.pack(pady=5)
        label = tk.Label(frame, text=label_text, font=("Arial", 14), bg="lightgreen")
        label.pack(side="left", padx=5)
        entry = tk.Entry(frame, font=("Arial", 14))
        entry.pack(side="left", padx=5)
        return entry

    def fetch_devices(self):
        try:
            response = requests.get(API_URL_LIST)
            response.raise_for_status()
            devices = response.json()
            self.display_devices(devices)
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"Failed to retrieve devices: {e}")

    def display_devices(self, devices):
        for row in self.tree.get_children():
            self.tree.delete(row)

        self.device_data.clear()

        for index, device in enumerate(devices):
            item_id = self.tree.insert("", "end", values=(device['name'], device['ip_address']))
            self.device_data[item_id] = device['id']

    def add_device(self):
        name = self.name_entry.get()
        ip_address = self.ip_entry.get()

        if not name or not ip_address:
            messagebox.showwarning("Input Error", "Please enter both device name and IP address!")
            return

        new_device = {
            "name": name,
            "ip_address": ip_address
        }

        try:
            response = requests.post(API_URL_ADD, json=new_device)
            response.raise_for_status()
            messagebox.showinfo("Success", "Device added successfully!")
            self.name_entry.delete(0, tk.END)
            self.ip_entry.delete(0, tk.END)
            self.fetch_devices()
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"Failed to add device: {e}")


    def delete_device(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Selection Error", "Please select a device to delete!")
            return

        device_id = self.device_data.get(selected_item[0])

        if not device_id:
            messagebox.showerror("Error", "Could not retrieve device ID!")
            return

        confirmation = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete this device?")
        if not confirmation:
            return

        try:
            response = requests.delete(API_URL_DELETE, json={"device_id": device_id})
            response.raise_for_status()
            messagebox.showinfo("Success", "Device deleted successfully!")
            self.fetch_devices()
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"Failed to delete device: {e}")

    def switch_back(self):
        from windows.main_window import MainWindow
        self.master.switch_frame(MainWindow)

