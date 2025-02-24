import tkinter as tk
from tkinter import ttk, messagebox
import requests

API_URL_EMAILS = "http://127.0.0.1:5000/api/email/list"
API_URL_ADD_EMAIL = "http://127.0.0.1:5000/api/email"
API_URL_DELETE_EMAIL = "http://127.0.0.1:5000/api/email"

class EmailWindow(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.configure(bg="lightblue")

        self.label = tk.Label(self, text="Active emails", font=("Arial", 20), bg="lightblue")
        self.label.pack(pady=10)

        table_frame = tk.Frame(self, bg="lightblue")
        table_frame.pack(pady=10)

        self.tree = ttk.Treeview(table_frame, columns=("Email",), show="headings", height=15)
        self.tree.column("Email", width=700, anchor="center")
        self.tree.heading("Email", text="Email")
        self.tree.pack(fill="both", padx=10, pady=1)

        button_frame = tk.Frame(self, bg="lightblue")
        button_frame.pack(pady=10)

        self.fetch_button = tk.Button(button_frame, text="Fetch Emails", command=self.fetch_emails)
        self.fetch_button.pack(side="left", padx=5)

        self.delete_button = tk.Button(button_frame, text="Delete Selected Email", command=self.delete_email, bg="red", fg="white")
        self.delete_button.pack(side="left", padx=5)

        self.add_label = tk.Label(self, text="Add New Email", font=("Arial", 16), bg="lightblue")
        self.add_label.pack(pady=10)

        self.email_entry = self.create_labeled_entry("Email Address:")

        self.add_button = tk.Button(self, text="Add Email", command=self.add_email)
        self.add_button.pack(pady=10)

        self.back_button = tk.Button(self, text="Back to Main Window", command=self.switch_back)
        self.back_button.pack(side="bottom", pady=10)

    def create_labeled_entry(self, label_text):
        frame = tk.Frame(self, bg="lightblue")
        frame.pack(pady=5)
        label = tk.Label(frame, text=label_text, font=("Arial", 14), bg="lightblue")
        label.pack(side="left", padx=5)
        entry = tk.Entry(frame, font=("Arial", 14))
        entry.pack(side="left", padx=5)
        return entry

    def fetch_emails(self):
        """Dohvaća e-mailove sa servera i prikazuje ih u tablici."""
        try:
            response = requests.get(API_URL_EMAILS)
            response.raise_for_status()
            emails = response.json().get("emails", [])

            # Brisanje stare tablice
            for row in self.tree.get_children():
                self.tree.delete(row)

            # Dodavanje novih podataka
            for email in emails:
                self.tree.insert("", "end", values=(email,))

        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"Failed to retrieve emails: {e}")

    def add_email(self):
        """Dodaje novi e-mail pomoću API-ja."""
        email = self.email_entry.get()

        if not email:
            messagebox.showwarning("Input Error", "Please enter an email address!")
            return

        try:
            response = requests.post(API_URL_ADD_EMAIL, json={"email": email})
            response.raise_for_status()
            response_data = response.json()

            messagebox.showinfo("Success", response_data.get("message", "Email added successfully!"))
            self.email_entry.delete(0, tk.END)
            self.fetch_emails()  # Ažuriranje tablice
        
        except requests.exceptions.HTTPError as e:
            try:
                error_message = response.json().get("message", "Unknown error occurred!")
            except:
                error_message = str(e)
            messagebox.showerror("Error", error_message)

        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"Failed to add email: {e}")

    def delete_email(self):
        """Briše odabrani e-mail sa servera."""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Selection Error", "Please select an email to delete!")
            return

        email = self.tree.item(selected_item)["values"][0]  # Dohvaćanje e-maila iz odabrane stavke

        confirmation = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete this email: {email}?")
        if not confirmation:
            return

        try:
            response = requests.delete(API_URL_DELETE_EMAIL, json={"email": email})
            response.raise_for_status()
            response_data = response.json()

            messagebox.showinfo("Success", response_data.get("message", "Email deleted successfully!"))
            self.fetch_emails()  # Ažuriranje tablice
        
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"Failed to delete email: {e}")

    def switch_back(self):
        from windows.main_window import MainWindow
        self.master.switch_frame(MainWindow)
