import tkinter as tk
from tkinter import ttk, messagebox
from repositories.activo_repository import obtener_activos, obtener_activo_por_id, eliminar_activo_por_id
from gui.registro_activo import RegistroActivo
from gui.actualizar_activo import ActualizarActivo
from gui.maintenance_window import MaintenanceWindow

class Dashboard:
    def __init__(self, user):
        self.user = user
        self.window = tk.Tk()
        self.window.title("Dashboard - Gestión de Activos")
        self.window.geometry("1300x600")

        tk.Label(self.window, text=f"Bienvenido, {self.user.fullname}", font=("Arial", 16)).pack(pady=10)
        tk.Label(self.window, text=f"Rol: {self.user.role}", font=("Arial", 12)).pack(pady=5)

        button_frame = tk.Frame(self.window)
        button_frame.pack(pady=10)

        if self.user.role == "admin":
            tk.Button(button_frame, text="Mantenimiento", width=20,command=self.open_maintenance).grid(row=0, column=0, padx=5)
            tk.Button(button_frame, text="Agregar Activo", width=20, command=self.abrir_registro_activo).grid(row=0, column=1, padx=5)
        tk.Button(button_frame, text="Cerrar sesión", width=20, command=self.logout).grid(row=0, column=2, padx=5)

        self.columnas = {
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

        if self.user.role == "admin":
            self.columnas["acciones"] = "Acciones"

        self.tree = ttk.Treeview(
            self.window,
            columns=list(self.columnas.keys()),
            show="headings",
            height=15
        )

        for col, heading in self.columnas.items():
            self.tree.heading(col, text=heading)
            self.tree.column(col, width=80, anchor="center")

        self.tree.pack(padx=10, pady=10, fill="both", expand=True)

        if self.user.role == "admin":
            self.tree.bind("<Double-1>", self.on_double_click)

        self.cargar_activos()
        self.window.mainloop()
    
    def open_maintenance(self):
        MaintenanceWindow(self.window,on_update=self.cargar_activos)

    def abrir_registro_activo(self):
        RegistroActivo(self.window, quien_registro=self.user.fullname, on_registro_exitoso=self.cargar_activos)

    def cargar_activos(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        activos = obtener_activos()
        for activo in activos:
            values = [
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
            ]
            if self.user.role == "admin":
                values.append("Actualizar | Eliminar")  # Mostrar texto en la columna
                self.tree.insert("", "end", iid=str(activo["_id"]), values=values)  # Usar el _id como iid
            else:
                self.tree.insert("", "end", values=values)

    def on_double_click(self, event):
        item = self.tree.identify_row(event.y)
        if item:
            activo_id = item  # El iid es el _id del activo
            self.mostrar_acciones(activo_id)

    def mostrar_acciones(self, activo_id):
        activo = obtener_activo_por_id(activo_id)
        if not activo:
            messagebox.showerror("Error", "Activo no encontrado.")
            return

        accion_win = tk.Toplevel(self.window)
        accion_win.title("Acciones del Activo")
        accion_win.geometry("300x150")

        tk.Label(accion_win, text="Seleccione una acción para el activo:").pack(pady=10)
        tk.Button(accion_win, text="Actualizar", width=20, command=lambda: self.actualizar_activo(activo, accion_win)).pack(pady=5)
        tk.Button(accion_win, text="Eliminar", width=20, command=lambda: self.eliminar_activo(activo_id, accion_win)).pack(pady=5)

    def actualizar_activo(self, activo, ventana):
        ventana.destroy()
        ActualizarActivo(self.window, activo, on_actualizacion_exitosa=self.cargar_activos)

    def eliminar_activo(self, activo_id, ventana):
        confirm = messagebox.askyesno("Confirmar", "¿Estás seguro de que deseas eliminar este activo?")
        if confirm:
            eliminar_activo_por_id(activo_id)
            ventana.destroy()
            self.cargar_activos()

    def logout(self):
        self.window.destroy()
        from app.main import HomePage
        app = HomePage()
        app.mainloop()
