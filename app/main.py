import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os
from gui.login_window import LoginView
from gui.register_window import RegisterWindow

class HomePage(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gestión de Activos - Inicio")
        self.geometry("800x400")
        self.resizable(False, False)

        # Frame Izquierdo (Botones)
        left_frame = tk.Frame(self, width=400, bg="#f0f0f0")
        left_frame.pack(side="left", fill="both", expand=True)
        s = ttk.Style()
        s.configure("Peligro.TButton", foreground="#ff0000")
        s.map("Peligro.TButton", foreground=[("active", "#FFA500")])
        tk.Label(left_frame, text="Bienvenido", font=("Arial", 20), bg="#f0f0f0").pack(pady=40)

        login_btn = ttk.Button(left_frame, text="Login", command=self.go_to_login, style="Peligro.TButton")
        login_btn.pack(pady=10, ipadx=10, ipady=5)

        signup_btn = ttk.Button(left_frame, text="Sign Up", command=self.go_to_signup)
        signup_btn.pack(pady=10, ipadx=10, ipady=5)

        # Frame Derecho (Imagen)
        right_frame = tk.Frame(self, width=400, bg="white")
        right_frame.pack(side="right", fill="both", expand=True)
        try:
            base_path = os.path.dirname(os.path.abspath(__file__))
            # Ajusta la ruta para que apunte correctamente al directorio assets
            image_path = os.path.abspath(os.path.join(base_path, "..", "assets", "fondo.jpg"))
            print("Ruta de la imagen:", image_path)
            image = Image.open(image_path)
            image = image.resize((400, 400))
            self.photo = ImageTk.PhotoImage(image)
            label = tk.Label(right_frame, image=self.photo, bg="white")
            label.pack(fill="both", expand=True)
        except Exception as e:
            error_label = tk.Label(right_frame, text="No se pudo cargar la imagen.", bg="white")
            error_label.pack(pady=180)

    def go_to_login(self):
        print("Ir al login")  # Aquí puedes abrir la ventana de login
        self.destroy()  # Cierra la ventana actual
        login_app = LoginView()
        login_app.mainloop()

    def go_to_signup(self):
        print("Ir al registro")
        reg_window = tk.Toplevel()
        RegisterWindow(reg_window)

if __name__ == "__main__":
    app = HomePage()
    app.mainloop()
