from repositories.assets_repository import maintenances_collection, assets_collection
from bson.objectid import ObjectId
from datetime import datetime

class MaintenanceModel:
    @staticmethod
    def add_maintenance(asset_id, description, performed_by, maintenance_type):
        maintenance = {
            "asset_id": ObjectId(asset_id),
            "description": description,
            "performed_by": performed_by,
            "maintenance_type": maintenance_type,
            "date": datetime.now()
        }
        maintenances_collection.insert_one(maintenance)

        # Actualizar campo de último mantenimiento en el activo
        assets_collection.update_one(
            {"_id": ObjectId(asset_id)},
            {"$set": {"last_maintenance": maintenance["date"]}}
        )

    @staticmethod
    def get_maintenances_for_asset(asset_id):
        return list(maintenances_collection.find({"asset_id": ObjectId(asset_id)}))

    @staticmethod
    def update_asset_status(asset_id, status):
        assets_collection.update_one(
            {"_id": ObjectId(asset_id)},
            {"$set": {"estado": status}}
        )
        
        
    # En maintenance_model.py
    @staticmethod
    def delete_maintenance(maintenance_id):
        maintenances_collection.delete_one({"_id": ObjectId(maintenance_id)})

    @staticmethod
    def update_maintenance(maintenance_id, description, performed_by, maintenance_type):
        maintenances_collection.update_one(
            {"_id": ObjectId(maintenance_id)},
            {"$set": {
                "description": description,
                "performed_by": performed_by,
                "maintenance_type": maintenance_type
            }}
        )
