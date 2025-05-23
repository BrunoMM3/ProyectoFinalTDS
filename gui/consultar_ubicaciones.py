# Crear el archivo gui/consultar_ubicaciones.py que mostrará las ubicaciones asignadas en una tabla.

import tkinter as tk
from tkinter import ttk
from repositories.location_repository import obtener_ubicaciones

class ConsultarUbicaciones(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Ubicaciones asignadas")
        self.geometry("800x400")

        self.tree = ttk.Treeview(self, columns=("codigo", "ubicacion", "encargado", "fecha"), show="headings")
        self.tree.heading("codigo", text="Código Interno")
        self.tree.heading("ubicacion", text="Ubicación")
        self.tree.heading("encargado", text="Encargado")
        self.tree.heading("fecha", text="Fecha de Asignación")

        self.tree.column("codigo", width=150, anchor="center")
        self.tree.column("ubicacion", width=200, anchor="center")
        self.tree.column("encargado", width=150, anchor="center")
        self.tree.column("fecha", width=150, anchor="center")

        self.tree.pack(padx=10, pady=10, fill="both", expand=True)

        self.cargar_ubicaciones()

    def cargar_ubicaciones(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        ubicaciones = obtener_ubicaciones()
        for ubicacion in ubicaciones:
            self.tree.insert("", "end", values=(
                ubicacion.get("codigo_interno", ""),
                ubicacion.get("ubicacion", ""),
                ubicacion.get("encargado", ""),
                ubicacion.get("fecha_asignacion", "")
            ))
