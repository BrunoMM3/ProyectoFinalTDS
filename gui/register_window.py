import tkinter as tk
from tkinter import ttk, messagebox
from controllers.register_controller import RegisterController

class RegisterWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Registro de Usuario")
        self.root.geometry("400x400")
        self.controller = RegisterController()

        tk.Label(root, text="Registro de Usuario", font=("Arial", 16)).pack(pady=10)

        self.entries = {}
        fields = ["Username", "Password", "Fullname", "Email"]
        for field in fields:
            tk.Label(root, text=field).pack()
            entry = tk.Entry(root, show="*" if field == "Password" else None)
            entry.pack()
            self.entries[field.lower()] = entry

        # Campo para código de administrador
        tk.Label(root, text="Código de Administrador (opcional)").pack()
        self.admin_code_entry = tk.Entry(root)
        self.admin_code_entry.pack()

        tk.Button(root, text="Registrarse", command=self.register).pack(pady=20)

    def register(self):
        username = self.entries["username"].get()
        password = self.entries["password"].get()
        fullname = self.entries["fullname"].get()
        email = self.entries["email"].get()
        admin_code = self.admin_code_entry.get()

        # Cambia "1234" por el código que desees
        role = "admin" if admin_code == "1234" else "user"

        success, msg = self.controller.register_user(username, password, fullname, email, role)
        if success:
            messagebox.showinfo("Éxito", msg)
            self.root.destroy()
        else:
            messagebox.showerror("Error", msg)