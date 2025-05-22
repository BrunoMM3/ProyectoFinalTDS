from models.maintenance_model import MaintenanceModel

class MaintenanceController:
    def __init__(self):
        self.model = MaintenanceModel

    def register_maintenance(self, asset_id, description, performed_by, maintenance_type):
        try:
            self.model.add_maintenance(asset_id, description, performed_by, maintenance_type)
            return True, "Mantenimiento registrado con éxito."
        except Exception as e:
            return False, str(e)

    def change_asset_status(self, asset_id, new_status):
        try:
            self.model.update_asset_status(asset_id, new_status)
            return True, "Estado del activo actualizado."
        except Exception as e:
            return False, str(e)

    def get_maintenance_history(self, asset_id):
        return self.model.get_maintenances_for_asset(asset_id)