# gui/registro_activo.py

import tkinter as tk
from tkinter import messagebox, ttk
from tkcalendar import DateEntry
from repositories.activo_repository import insertar_activo, existe_codigo_interno

class RegistroActivo(tk.Toplevel):
    def __init__(self, master, quien_registro, on_registro_exitoso=None):
        super().__init__(master)
        self.title("Registrar nuevo activo")
        self.geometry("500x600")
        self.quien_registro = quien_registro
        self.on_registro_exitoso = on_registro_exitoso

        self.campos = {}
        labels = [
            "nombre", "descripcion", "codigo_interno", "categoria",
            "marca", "modelo", "numero_serie", "estado", "Precio"
        ]

        row = 0
        for campo in labels:
            tk.Label(self, text=campo.replace("_", " ").capitalize() + ":").grid(row=row, column=0, sticky="w", padx=10, pady=5)
            if campo == "estado":
                var = tk.StringVar()
                combobox = ttk.Combobox(self, textvariable=var, values=["operativo", "en reparación", "dado de baja"], state="readonly", width=37)
                combobox.current(0)
                combobox.grid(row=row, column=1, padx=10, pady=5)
                self.campos[campo] = var
            else:
                var = tk.StringVar()
                entry = tk.Entry(self, textvariable=var, width=40)
                entry.grid(row=row, column=1, padx=10, pady=5)
                self.campos[campo] = var
            row += 1

        tk.Label(self, text="Fecha adquisición:").grid(row=row, column=0, sticky="w", padx=10, pady=5)
        self.fecha_adquisicion = DateEntry(self, width=37, date_pattern='yyyy-mm-dd')
        self.fecha_adquisicion.grid(row=row, column=1, padx=10, pady=5)
        row += 1

        tk.Button(self, text="Registrar activo", command=self.registrar_activo).grid(row=row, columnspan=2, pady=20)

    def registrar_activo(self):
        try:
            datos = {k: v.get() for k, v in self.campos.items()}

            if not all(datos.values()):
                messagebox.showwarning("Campos incompletos", "Todos los campos son obligatorios.")
                return

            # Validar duplicado por código interno
            if existe_codigo_interno(datos["codigo_interno"]):
                messagebox.showerror("Código duplicado", "El código interno ya existe. Usa uno diferente.")
                return

            # Validar valor numérico positivo
            datos["valor"] = float(datos["valor"])
            if datos["valor"] <= 0:
                messagebox.showerror("Valor inválido", "El valor debe ser mayor a 0.")
                return

            datos["fecha_adquisicion"] = self.fecha_adquisicion.get_date().strftime("%Y-%m-%d")
            datos["quien_registro"] = self.quien_registro

            insertar_activo(datos)
            messagebox.showinfo("Éxito", "Activo registrado correctamente.")
            if self.on_registro_exitoso:
                self.on_registro_exitoso()
            self.destroy()

        except ValueError as e:
            messagebox.showerror("Error", f"Datos inválidos: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo registrar el activo: {e}")
