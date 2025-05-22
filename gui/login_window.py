import tkinter as tk
from tkinter import messagebox
from controllers.login_controller import LoginController
from gui.dashboard import Dashboard
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class LoginView:
    def __init__(self, root, main_window=None):
        self.root = root
        self.root.title("Iniciar Sesión")
        self.root.geometry("400x300")
        self.main_window = main_window
        self.controller = LoginController()

        # Etiquetas y campos
        tk.Label(self.root, text="Usuario:").pack(pady=(20, 5))
        self.username_entry = tk.Entry(self.root)
        self.username_entry.pack()

        tk.Label(self.root, text="Contraseña:").pack(pady=(10, 5))
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.pack()

        # Botón de login
        tk.Button(self.root, text="Iniciar Sesión", command=self.login).pack(pady=20)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if not username or not password:
            messagebox.showerror("Error", "Por favor, complete todos los campos.")
            return
        user = self.controller.login_user(username, password)
        if user:
            messagebox.showinfo("Éxito", f"Bienvenido, {user.fullname}")
            self.root.destroy()
            if self.main_window:
                self.main_window.destroy()   # Cierra ventana login
            Dashboard(user)      # Lanza el dashboard
        else:
            messagebox.showerror("Error", "Credenciales incorrectas")

if __name__ == "__main__":
    app = LoginView()
    app.mainloop()
