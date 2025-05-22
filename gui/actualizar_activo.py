import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkcalendar import DateEntry
from bson import ObjectId
from repositories.activo_repository import actualizar_activo_por_id

class ActualizarActivo(tk.Toplevel):
    def __init__(self, master, activo, on_actualizacion_exitosa=None):
        super().__init__(master)
        self.title("Actualizar activo")
        self.geometry("500x650")
        self.activo = activo
        self.on_actualizacion_exitosa = on_actualizacion_exitosa

        self.campos = {}
        row = 0

        # Campos de texto
        for key in ["nombre", "descripcion", "codigo_interno", "categoria", "marca", "modelo", "numero_serie", "valor"]:
            tk.Label(self, text=key.replace("_", " ").capitalize() + ":").grid(row=row, column=0, sticky="w", padx=10, pady=5)
            var = tk.StringVar(value=str(activo.get(key, "")))
            entry = tk.Entry(self, textvariable=var, width=40)
            entry.grid(row=row, column=1, padx=10, pady=5)
            self.campos[key] = var
            row += 1

        # Estado (opciones)
        tk.Label(self, text="Estado:").grid(row=row, column=0, sticky="w", padx=10, pady=5)
        self.estado_var = tk.StringVar(value=activo.get("estado", ""))
        self.estado_combo = ttk.Combobox(
            self,
            textvariable=self.estado_var,
            state="readonly",
            values=["operativo", "en reparación", "dado de baja"]
        )
        self.estado_combo.grid(row=row, column=1, padx=10, pady=5)
        row += 1

        # Fecha de adquisición
        tk.Label(self, text="Fecha adquisición:").grid(row=row, column=0, sticky="w", padx=10, pady=5)
        self.fecha_adquisicion = DateEntry(self, width=37, date_pattern='yyyy-mm-dd')
        self.fecha_adquisicion.set_date(activo.get("fecha_adquisicion", ""))
        self.fecha_adquisicion.grid(row=row, column=1, padx=10, pady=5)
        row += 1

        # Botón de actualizar
        tk.Button(self, text="Actualizar activo", command=self.actualizar_activo).grid(row=row, columnspan=2, pady=20)

    def actualizar_activo(self):
        try:
            datos_actualizados = {k: v.get() for k, v in self.campos.items()}
            datos_actualizados["estado"] = self.estado_var.get()
            datos_actualizados["fecha_adquisicion"] = self.fecha_adquisicion.get_date().strftime("%Y-%m-%d")

            # Validar y convertir el valor
            valor = float(datos_actualizados["valor"])
            if valor < 0:
                raise ValueError("El valor debe ser positivo.")
            datos_actualizados["valor"] = valor

            # Convertir el _id si es string
            activo_id = self.activo["_id"]
            if isinstance(activo_id, str):
                activo_id = ObjectId(activo_id)

            actualizar_activo_por_id(activo_id, datos_actualizados)
            messagebox.showinfo("Éxito", "Activo actualizado correctamente.")
            if self.on_actualizacion_exitosa:
                self.on_actualizacion_exitosa()
            self.destroy()
        except ValueError as e:
            messagebox.showerror("Error", f"Datos inválidos: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo actualizar el activo: {e}")
