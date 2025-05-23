import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
from controllers.asset_controller import AssetController

class AdvancedQueryWindow(tk.Toplevel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.title("Consultas Avanzadas de Activos")
        self.geometry("900x550")
        self.asset_controller = AssetController()
        self.results = []  # Almacena los últimos resultados

        # Filtros
        filter_frame = tk.LabelFrame(self, text="Filtros")
        filter_frame.pack(fill=tk.X, padx=10, pady=10)

        tk.Label(filter_frame, text="Estado:").grid(row=0, column=0, padx=5, pady=5)
        self.status_combo = ttk.Combobox(filter_frame, values=["", "operativo", "en reparación", "dado de baja"])
        self.status_combo.grid(row=0, column=1, padx=5)

        tk.Label(filter_frame, text="Ubicación:").grid(row=0, column=2, padx=5)
        self.location_entry = tk.Entry(filter_frame)
        self.location_entry.grid(row=0, column=3, padx=5)

        tk.Label(filter_frame, text="Asignado a:").grid(row=0, column=4, padx=5)
        self.user_entry = tk.Entry(filter_frame)
        self.user_entry.grid(row=0, column=5, padx=5)

        tk.Button(filter_frame, text="Buscar", command=self.perform_query).grid(row=0, column=6, padx=10)

        # Tabla de resultados
        self.tree = ttk.Treeview(self, columns=("nombre", "ubicacion", "estado", "encargado"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col.capitalize())
            self.tree.column(col, width=200)
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Botones de exportación
        export_frame = tk.Frame(self)
        export_frame.pack(pady=5)

        tk.Button(export_frame, text="Exportar a CSV", command=self.export_csv).pack(side=tk.LEFT, padx=10)
        tk.Button(export_frame, text="Exportar a Excel", command=self.export_excel).pack(side=tk.LEFT)

    def perform_query(self):
        status = self.status_combo.get()
        location = self.location_entry.get()
        assigned_to = self.user_entry.get()

        filters = {}
        if status:
            filters["estado"] = status
        if location:
            filters["ubicacion"] = location
        if assigned_to:
            filters["encargado"] = assigned_to

        self.results = self.asset_controller.advanced_query(filters)

        for i in self.tree.get_children():
            self.tree.delete(i)

        for asset in self.results:
            ubicacion, encargado = self.asset_controller.get_location_info(asset["_id"])
            self.tree.insert("", "end", values=(
                asset.get("nombre", "Sin nombre"),
                ubicacion,
                asset.get("estado", "Desconocido"),
                encargado
            ))

    def export_csv(self):
        if not self.results:
            messagebox.showwarning("Sin datos", "Primero realiza una búsqueda.")
            return
        path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV", "*.csv")])
        if path:
            df = pd.DataFrame(self.results)
            df.to_csv(path, index=False)
            messagebox.showinfo("Exportado", "Datos exportados a CSV correctamente.")

    def export_excel(self):
        if not self.results:
            messagebox.showwarning("Sin datos", "Primero realiza una búsqueda.")
            return
        path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel", "*.xlsx")])
        if path:
            df = pd.DataFrame(self.results)
            df.to_excel(path, index=False)
            messagebox.showinfo("Exportado", "Datos exportados a Excel correctamente.")