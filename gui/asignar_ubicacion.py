import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from repositories.activo_repository import obtener_activos
from repositories.location_repository import guardar_ubicacion

class AsignarUbicacion(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Asignar ubicación a activo")
        self.geometry("500x400")

        tk.Label(self, text="Seleccionar activo:").pack(pady=5)
        self.activo_seleccionado = tk.StringVar()
        self.combo_activos = ttk.Combobox(self, textvariable=self.activo_seleccionado, width=60, state="readonly")
        self.combo_activos.pack(pady=5)

        self.activos = obtener_activos()
        self.activo_por_nombre = {self.formatear_activo(a): a for a in self.activos}
        self.combo_activos["values"] = list(self.activo_por_nombre.keys())

        tk.Label(self, text="Ubicación:").pack(pady=5)
        self.ubicacion_entry = tk.Entry(self, width=50)
        self.ubicacion_entry.pack(pady=5)

        tk.Label(self, text="Encargado:").pack(pady=5)
        self.encargado_entry = tk.Entry(self, width=50)
        self.encargado_entry.pack(pady=5)

        tk.Label(self, text="Fecha asignación:").pack(pady=5)
        self.fecha_asignacion = DateEntry(self, date_pattern="yyyy-mm-dd", width=47)
        self.fecha_asignacion.pack(pady=5)

        tk.Button(self, text="Guardar ubicación", command=self.guardar_ubicacion).pack(pady=20)

    def formatear_activo(self, activo):
        return f"{activo.get('nombre')} ({activo.get('codigo_interno')})"

    def guardar_ubicacion(self):
        nombre_activo = self.activo_seleccionado.get()
        if not nombre_activo:
            messagebox.showwarning("Advertencia", "Debe seleccionar un activo.")
            return

        activo = self.activo_por_nombre[nombre_activo]
        ubicacion = self.ubicacion_entry.get().strip()
        encargado = self.encargado_entry.get().strip()
        fecha = self.fecha_asignacion.get_date().strftime("%Y-%m-%d")

        if not ubicacion or not encargado:
            messagebox.showwarning("Advertencia", "Todos los campos son obligatorios.")
            return

        try:
            guardar_ubicacion({
                "activo_id": activo["_id"],
                "codigo_interno": activo["codigo_interno"],
                "ubicacion": ubicacion,
                "encargado": encargado,
                "fecha_asignacion": fecha
            })
            messagebox.showinfo("Éxito", "Ubicación asignada correctamente.")
            self.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar la ubicación: {e}")
