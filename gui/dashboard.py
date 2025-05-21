# gui/dashboard.py

import tkinter as tk
from tkinter import ttk
from repositories.activo_repository import obtener_activos
from gui.registro_activo import RegistroActivo

class Dashboard:
    def __init__(self, user):
        self.user = user
        self.window = tk.Tk()
        self.window.title("Dashboard - Gestión de Activos")
        self.window.geometry("1200x600")

        # Encabezado
        tk.Label(self.window, text=f"Bienvenido, {self.user.fullname}", font=("Arial", 16)).pack(pady=10)
        tk.Label(self.window, text=f"Rol: {self.user.role}", font=("Arial", 12)).pack(pady=5)

        # Botones
        button_frame = tk.Frame(self.window)
        button_frame.pack(pady=10)

        if self.user.role == "admin":
            tk.Button(button_frame, text="Gestionar Usuarios", width=20).grid(row=0, column=0, padx=5)
        tk.Button(button_frame, text="Agregar Activo", width=20, command=self.abrir_registro_activo).grid(row=0, column=1, padx=5)
        tk.Button(button_frame, text="Cerrar sesión", width=20, command=self.logout).grid(row=0, column=2, padx=5)

        # Tabla
        self.tree = ttk.Treeview(self.window, columns=(
            "nombre", "descripcion", "codigo_interno", "categoria", "marca", 
            "modelo", "numero_serie", "estado", "fecha_adquisicion", "valor", "quien_registro"
        ), show="headings", height=15)

        columnas = {
            "nombre": "Nombre",
            "descripcion": "Descripción",
            "codigo_interno": "Código Interno",
            "categoria": "Categoría",
            "marca": "Marca",
            "modelo": "Modelo",
            "numero_serie": "N° Serie",
            "estado": "Estado",
            "fecha_adquisicion": "Fecha de Adquisición",
            "valor": "Precio",
            "quien_registro": "Registrado por"
        }

        for col, heading in columnas.items():
            self.tree.heading(col, text=heading)
            self.tree.column(col, width=100, anchor="center")

        self.tree.pack(padx=10, pady=10, fill="both", expand=True)

        self.cargar_activos()

        self.window.mainloop()
    
    def abrir_registro_activo(self):
        RegistroActivo(self.window, quien_registro=self.user.fullname, on_registro_exitoso=self.cargar_activos)

    def cargar_activos(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        activos = obtener_activos()
        for activo in activos:
            self.tree.insert("", "end", values=(
                activo.get("nombre", ""),
                activo.get("descripcion", ""),
                activo.get("codigo_interno", ""),
                activo.get("categoria", ""),
                activo.get("marca", ""),
                activo.get("modelo", ""),
                activo.get("numero_serie", ""),
                activo.get("estado", ""),
                activo.get("fecha_adquisicion", ""),
                f"${activo.get('valor', 0):,.2f}",
                activo.get("quien_registro", "")
            ))


    def logout(self):
        self.window.destroy()
        from app.main import HomePage
        app = HomePage()
        app.mainloop()
