from models.asset_model import AssetModel

class AssetController:
    def __init__(self):
        self.model = AssetModel

    def add_asset(self, name, description, serial_number, purchase_date, location):
        try:
            asset_id = self.model.add_asset(name, description, serial_number, purchase_date, location)
            return True, f"Activo registrado con ID: {asset_id}"
        except Exception as e:
            return False, f"Error al registrar el activo: {str(e)}"

    def get_all_assets(self):
        return self.model.get_all_assets()

    def update_asset(self, asset_id, updates):
        try:
            self.model.update_asset(asset_id, updates)
            return True, "Activo actualizado correctamente"
        except Exception as e:
            return False, f"Error al actualizar: {str(e)}"

    def delete_asset(self, asset_id):
        try:
            self.model.delete_asset(asset_id)
            return True, "Activo eliminado"
        except Exception as e:
            return False, f"Error al eliminar: {str(e)}"
    
    def get_assets_by_user(self, username):
        return self.model.get_assets_by_user(username)

    def advanced_query(self, filters: dict):
        return self.model.query_assets(filters)