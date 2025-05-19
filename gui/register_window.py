import tkinter as tk
from tkinter import ttk, messagebox
from controllers.register_controller import RegisterController

class RegisterWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Registro de Usuario")
        self.root.geometry("400x350")
        self.controller = RegisterController()

        tk.Label(root, text="Registro de Usuario", font=("Arial", 16)).pack(pady=10)

        self.entries = {}
        fields = ["Username", "Password", "Fullname", "Email"]
        for field in fields:
            tk.Label(root, text=field).pack()
            entry = tk.Entry(root, show="*" if field == "Password" else None)
            entry.pack()
            self.entries[field.lower()] = entry

        tk.Button(root, text="Registrarse", command=self.register).pack(pady=20)

    def register(self):
        username = self.entries["username"].get()
        password = self.entries["password"].get()
        fullname = self.entries["fullname"].get()
        email = self.entries["email"].get()

        success, msg = self.controller.register_user(username, password, fullname, email)
        if success:
            messagebox.showinfo("Éxito", msg)
            self.root.destroy()
        else:
            messagebox.showerror("Error", msg)
