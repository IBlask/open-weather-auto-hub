import tkinter as tk
from tkinter import ttk, messagebox
import requests

API_URL_LIST = "http://127.0.0.1:5000/api/automation-request/list"
API_URL_ADD = "http://127.0.0.1:5000/api/automation-request"
API_URL_DELETE = "http://127.0.0.1:5000/api/automation-request"
API_URL_DEVICE = "http://127.0.0.1:5000/api/automation-device"
API_URL_DEVICE_LIST = "http://127.0.0.1:5000/api/automation-device/list"

class AutomationRequestWindow(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.configure(bg="lightyellow")

        self.label = tk.Label(self, text="Automation Requests", font=("Arial", 20), bg="lightyellow")
        self.label.pack(pady=10)

        table_frame = tk.Frame(self, bg="lightyellow")
        table_frame.pack(pady=10)

        columns = ("Device Name", "Name", "Trigger", "Trigger Value", "Trigger Operator", "Port", "URI", "Body")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)
        for col in columns:
            self.tree.column(col, width=100, anchor="center")
            self.tree.heading(col, text=col)
        self.tree.pack(fill="both", padx=10, pady=1)
        self.tree.bind("<Double-1>", self.on_row_double_click)

        self.request_data = {}

        button_frame = tk.Frame(self, bg="lightyellow")
        button_frame.pack(pady=10)

        self.fetch_button = tk.Button(button_frame, text="Fetch Requests", command=self.fetch_requests)
        self.fetch_button.pack(side="left", padx=5)

        self.delete_button = tk.Button(button_frame, text="Delete Selected Request", command=self.delete_request, bg="red", fg="white")
        self.delete_button.pack(side="left", padx=5)

        self.add_label = tk.Label(self, text="Add New Request", font=("Arial", 16), bg="lightyellow")
        self.add_label.pack(pady=10)

        form_frame = tk.Frame(self, bg="lightyellow")
        form_frame.pack(pady=10)

        self.create_labeled_entry(form_frame, "Name:", 0, 0)
        self.create_labeled_entry(form_frame, "Trigger:", 1, 0)
        self.create_labeled_entry(form_frame, "Trigger Operator:", 2, 0)
        self.create_labeled_entry(form_frame, "Trigger Value:", 3, 0)
        self.create_device_dropdown(form_frame, "Device:", 0, 1)
        self.create_labeled_entry(form_frame, "Port:", 1, 1)
        self.create_labeled_entry(form_frame, "URI:", 2, 1)
        self.create_labeled_entry(form_frame, "Body:", 3, 1)

        self.add_button = tk.Button(self, text="Add Request", command=self.add_request)
        self.add_button.pack(pady=10)

        self.back_button = tk.Button(self, text="Back to Main Window", command=self.switch_back)
        self.back_button.pack(side="bottom", pady="10")

    def create_labeled_entry(self, parent, label_text, row, column):
        label = tk.Label(parent, text=label_text, font=("Arial", 14), bg="lightyellow")
        label.grid(row=row, column=column*2, padx=5, pady=5, sticky="e")
        entry = tk.Entry(parent, font=("Arial", 14), width=30)
        entry.grid(row=row, column=column*2+1, padx=5, pady=5, sticky="w")
        setattr(self, f"{label_text.lower().replace(' ', '_').replace(':', '')}_entry", entry)

    def create_device_dropdown(self, parent, label_text, row, column):
        label = tk.Label(parent, text=label_text, font=("Arial", 14), bg="lightyellow")
        label.grid(row=row, column=column*2, padx=5, pady=5, sticky="e")
        self.device_var = tk.StringVar()
        self.device_dropdown = ttk.Combobox(parent, textvariable=self.device_var, font=("Arial", 14), width=30)
        self.device_dropdown.grid(row=row, column=column*2+1, padx=5, pady=5, sticky="w")
        self.fetch_devices()

    def fetch_devices(self):
        try:
            response = requests.get(API_URL_DEVICE_LIST)
            response.raise_for_status()
            devices = response.json()
            self.device_dropdown['values'] = [device['name'] for device in devices]
            self.device_id_map = {device['name']: device['id'] for device in devices}
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"Failed to retrieve devices: {e}")

    def fetch_requests(self):
        try:
            response = requests.get(API_URL_LIST)
            response.raise_for_status()
            requests_data = response.json()
            self.display_requests(requests_data)
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"Failed to retrieve requests: {e}")

    def fetch_device_name(self, device_id):
        try:
            response = requests.get(f"{API_URL_DEVICE}/{device_id}")
            response.raise_for_status()
            device_data = response.json()
            return device_data['name']
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"Failed to retrieve device name: {e}")
            return "Unknown"

    def display_requests(self, requests_data):
        for row in self.tree.get_children():
            self.tree.delete(row)

        self.request_data.clear()

        for index, request in enumerate(requests_data):
            device_name = self.fetch_device_name(request['device_id'])
            item_id = self.tree.insert("", "end", values=(
                device_name, request['name'], request['trigger'], 
                request['trigger_value'], request['trigger_operator'], request['port'], 
                request['uri'], request['body']
            ))
            self.request_data[item_id] = request['id']

    def add_request(self):
        device_name = self.device_var.get()
        device_id = self.device_id_map.get(device_name, "")
        new_request = {
            "device_id": device_id,
            "name": self.name_entry.get(),
            "trigger": self.trigger_entry.get(),
            "trigger_value": self.trigger_value_entry.get(),
            "trigger_operator": self.trigger_operator_entry.get(),
            "port": self.port_entry.get(),
            "uri": self.uri_entry.get(),
            "body": self.body_entry.get()
        }

        try:
            response = requests.post(API_URL_ADD, json=new_request)
            response.raise_for_status()
            response_data = response.json()

            messagebox.showinfo("Success", response_data.get("message", "Request added successfully!"))
            self.clear_entries()
            self.fetch_requests()
        
        except requests.exceptions.HTTPError as e:
            try:
                error_message = response.json().get("message", "Unknown error occurred!")
            except:
                error_message = str(e)
            messagebox.showerror("Error", error_message)

        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"Failed to add request: {e}")

    def delete_request(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Selection Error", "Please select a request to delete!")
            return

        request_id = self.request_data.get(selected_item[0])

        if not request_id:
            messagebox.showerror("Error", "Could not retrieve request ID!")
            return

        confirmation = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete this request?")
        if not confirmation:
            return

        try:
            response = requests.delete(f"{API_URL_DELETE}/{request_id}")
            response.raise_for_status()
            messagebox.showinfo("Success", "Request deleted successfully!")
            self.fetch_requests()
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"Failed to delete request: {e}")

    def clear_entries(self):
        self.device_var.set("")
        self.name_entry.delete(0, tk.END)
        self.trigger_entry.delete(0, tk.END)
        self.trigger_value_entry.delete(0, tk.END)
        self.trigger_operator_entry.delete(0, tk.END)
        self.port_entry.delete(0, tk.END)
        self.uri_entry.delete(0, tk.END)
        self.body_entry.delete(0, tk.END)

    def switch_back(self):
        from windows.main_window import MainWindow
        self.master.switch_frame(MainWindow)

    def on_row_double_click(self, event):
        item_id = self.tree.selection()[0]
        request_id = self.request_data[item_id]
        request_data = self.tree.item(item_id, "values")

        popup = tk.Toplevel(self)
        popup.title("Request Information")
        popup.geometry("600x400")

        canvas = tk.Canvas(popup)
        scrollbar = tk.Scrollbar(popup, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        labels = ["Device Name", "Name", "Trigger", "Trigger Value", "Trigger Operator", "Port", "URI", "Body"]
        for i, label_text in enumerate(labels):
            label = tk.Label(scrollable_frame, text=label_text, font=("Arial", 14), bg="lightyellow")
            label.grid(row=i, column=0, padx=5, pady=5, sticky="e")
            value = tk.Label(scrollable_frame, text=request_data[i], font=("Arial", 14), bg="lightyellow", wraplength=500)
            value.grid(row=i, column=1, padx=5, pady=5, sticky="w")