import tkinter as tk
from tkinter import ttk, messagebox
from controllers.asset_controller import AssetController
from controllers.maintenance_controller import MaintenanceController

class MaintenanceWindow(tk.Toplevel):
    def __init__(self, parent=None, on_update=None):
        super().__init__(parent)
        self.on_update = on_update
        self.title("Mantenimiento y Estado del Activo")
        self.geometry("800x600")

        self.asset_controller = AssetController()
        self.maintenance_controller = MaintenanceController()

        self.selected_asset_id = None

        self.create_widgets()
        self.load_assets()

    def create_widgets(self):
        # Label para activos
        tk.Label(self, text="Selecciona un activo").grid(row=0, column=0, sticky="w", padx=10, pady=5)

        # Treeview activos
        self.asset_tree = ttk.Treeview(self, columns=("name", "status"), show="headings", height=5)
        self.asset_tree.heading("name", text="Nombre")
        self.asset_tree.heading("status", text="Estado")
        self.asset_tree.column("name", width=250)
        self.asset_tree.column("status", width=100)
        self.asset_tree.grid(row=1, column=0, columnspan=2, sticky="ew", padx=10)
        self.asset_tree.bind("<<TreeviewSelect>>", self.on_asset_select)

        # Formulario mantenimiento
        form_frame = tk.LabelFrame(self, text="Registrar Mantenimiento")
        form_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=10)

        tk.Label(form_frame, text="Tipo:").grid(row=0, column=0, sticky="w", padx=5, pady=2)
        self.type_entry = ttk.Combobox(form_frame, values=["preventivo", "correctivo"])
        self.type_entry.grid(row=0, column=1, sticky="ew", padx=5, pady=2)

        tk.Label(form_frame, text="Descripción:").grid(row=1, column=0, sticky="w", padx=5, pady=2)
        self.desc_entry = tk.Entry(form_frame, width=50)
        self.desc_entry.grid(row=1, column=1, sticky="ew", padx=5, pady=2)

        tk.Label(form_frame, text="Realizado por:").grid(row=2, column=0, sticky="w", padx=5, pady=2)
        self.performed_by_entry = tk.Entry(form_frame)
        self.performed_by_entry.grid(row=2, column=1, sticky="ew", padx=5, pady=2)

        tk.Button(form_frame, text="Registrar", command=self.register_maintenance).grid(row=3, column=0, columnspan=2, pady=5)

        # Formulario cambio de estado
        state_frame = tk.LabelFrame(self, text="Actualizar Estado del Activo")
        state_frame.grid(row=2, column=1, sticky="ew", padx=10, pady=10)

        tk.Label(state_frame, text="Nuevo estado:").grid(row=0, column=0, sticky="w", padx=5, pady=2)
        self.state_entry = ttk.Combobox(state_frame, values=["operativo", "en reparación", "dado de baja"])
        self.state_entry.grid(row=0, column=1, sticky="ew", padx=5, pady=2)

        tk.Button(state_frame, text="Actualizar Estado", command=self.update_status).grid(row=1, column=0, columnspan=2, pady=5)

        # Label historial mantenimiento
        tk.Label(self, text="Historial de Mantenimiento").grid(row=3, column=0, columnspan=2, sticky="w", padx=10, pady=(10, 0))

        # Frame para historial con scrollbar
        history_frame = tk.Frame(self)
        history_frame.grid(row=4, column=0, columnspan=2, sticky="nsew", padx=10, pady=5)
        self.grid_rowconfigure(4, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.history_tree = ttk.Treeview(history_frame, columns=("id", "date", "type", "desc", "by"), show="headings")
        self.history_tree.heading("id", text="ID oculto")
        self.history_tree.heading("date", text="Fecha")
        self.history_tree.heading("type", text="Tipo")
        self.history_tree.heading("desc", text="Descripción")
        self.history_tree.heading("by", text="Realizado por")
        self.history_tree["displaycolumns"] = ("date", "type", "desc", "by")

        self.history_tree.column("date", width=120)
        self.history_tree.column("type", width=100)
        self.history_tree.column("desc", width=350)
        self.history_tree.column("by", width=150)

        self.history_tree.grid(row=0, column=0, sticky="nsew")

        scrollbar = ttk.Scrollbar(history_frame, orient="vertical", command=self.history_tree.yview)
        self.history_tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky="ns")

        history_frame.grid_rowconfigure(0, weight=1)
        history_frame.grid_columnconfigure(0, weight=1)

        # Botones editar y eliminar
        btn_frame = tk.Frame(self)
        btn_frame.grid(row=5, column=0, columnspan=2, pady=10)

        tk.Button(btn_frame, text="Editar Seleccionado", command=self.edit_selected).pack(side=tk.LEFT, padx=10)
        tk.Button(btn_frame, text="Eliminar Seleccionado", command=self.delete_selected).pack(side=tk.LEFT, padx=10)

    def get_selected_maintenance_id(self):
        selected = self.history_tree.selection()
        if not selected:
            messagebox.showwarning("Atención", "Selecciona un registro de mantenimiento.")
            return None
        return self.history_tree.item(selected[0], "values")[0]

    def delete_selected(self):
        maintenance_id = self.get_selected_maintenance_id()
        if not maintenance_id:
            return
        confirm = messagebox.askyesno("Confirmar", "¿Seguro que deseas eliminar este mantenimiento?")
        if confirm:
            success, msg = self.maintenance_controller.delete_maintenance(maintenance_id)
            messagebox.showinfo("Resultado", msg)
            if success:
                self.load_maintenance_history()

    def edit_selected(self):
        maintenance_id = self.get_selected_maintenance_id()
        if not maintenance_id:
            return
        selected = self.history_tree.item(self.history_tree.selection()[0])["values"]
        self.type_entry.set(selected[2])
        self.desc_entry.delete(0, tk.END)
        self.desc_entry.insert(0, selected[3])
        self.performed_by_entry.delete(0, tk.END)
        self.performed_by_entry.insert(0, selected[4])

        def save_edit():
            mtype = self.type_entry.get()
            desc = self.desc_entry.get()
            by = self.performed_by_entry.get()
            success, msg = self.maintenance_controller.update_maintenance(maintenance_id, desc, by, mtype)
            messagebox.showinfo("Resultado", msg)
            if success:
                self.load_maintenance_history()
                save_btn.destroy()

        save_btn = tk.Button(self, text="Guardar Edición", command=save_edit)
        save_btn.grid(row=6, column=0, columnspan=2, pady=5)

    def load_assets(self):
        for i in self.asset_tree.get_children():
            self.asset_tree.delete(i)
        assets = self.asset_controller.get_all_assets()
        for asset in assets:
            self.asset_tree.insert("", "end", iid=str(asset["_id"]), values=(asset["nombre"], asset["estado"]))

    def on_asset_select(self, event):
        selected = self.asset_tree.selection()
        if not selected:
            return
        self.selected_asset_id = selected[0]
        self.load_maintenance_history()

    def register_maintenance(self):
        if not self.selected_asset_id:
            messagebox.showwarning("Atención", "Selecciona un activo primero.")
            return
        mtype = self.type_entry.get()
        desc = self.desc_entry.get()
        by = self.performed_by_entry.get()
        if not all([mtype, desc, by]):
            messagebox.showerror("Error", "Completa todos los campos.")
            return
        success, msg = self.maintenance_controller.register_maintenance(self.selected_asset_id, desc, by, mtype)
        messagebox.showinfo("Resultado", msg)
        if success:
            self.load_maintenance_history()

    def update_status(self):
        if not self.selected_asset_id:
            messagebox.showwarning("Atención", "Selecciona un activo.")
            return
        new_state = self.state_entry.get()
        if not new_state:
            messagebox.showerror("Error", "Selecciona un nuevo estado.")
            return
        success, msg = self.maintenance_controller.change_asset_status(self.selected_asset_id, new_state)
        messagebox.showinfo("Resultado", msg)
        if success:
            self.load_assets()
            if self.on_update:
                self.on_update()

    def load_maintenance_history(self):
        for i in self.history_tree.get_children():
            self.history_tree.delete(i)
        history = self.maintenance_controller.get_maintenance_history(self.selected_asset_id)
        for entry in history:
            self.history_tree.insert("", "end", values=(
                str(entry["_id"]),
                entry["date"].strftime("%Y-%m-%d %H:%M"),
                entry["maintenance_type"],
                entry["description"],
                entry["performed_by"]
            ))
