import tkinter as tk
from tkinter import messagebox
from controllers.login_controller import LoginController
from gui.dashboard import Dashboard
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class LoginView(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Iniciar Sesión")
        self.geometry("400x300")
        self.controller = LoginController()

        # Etiquetas y campos
        tk.Label(self, text="Usuario:").pack(pady=(20, 5))
        self.username_entry = tk.Entry(self)
        self.username_entry.pack()

        tk.Label(self, text="Contraseña:").pack(pady=(10, 5))
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack()

        # Botón de login
        tk.Button(self, text="Iniciar Sesión", command=self.login).pack(pady=20)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if not username or not password:
            messagebox.showerror("Error", "Por favor, complete todos los campos.")
            return
        user = self.controller.login_user(username, password)
        if user:
            messagebox.showinfo("Éxito", f"Bienvenido, {user.fullname}")
            self.destroy()  # Cierra ventana login
            Dashboard(user)      # Lanza el dashboard
        else:
            messagebox.showerror("Error", "Credenciales incorrectas")


if __name__ == "__main__":
    app = LoginView()
    app.mainloop()
