from repositories.assets_repository import assets_collection
from bson.objectid import ObjectId
from datetime import datetime

class AssetModel:
    @staticmethod
    def add_asset(name, description, serial_number, purchase_date, location):
        asset = {
            "name": name,
            "description": description,
            "serial_number": serial_number,
            "purchase_date": purchase_date,
            "status": "operativo",  # estado por defecto
            "location": location,
            "assigned_to": None,
            "last_maintenance": None
        }
        result = assets_collection.insert_one(asset)
        return str(result.inserted_id)

    @staticmethod
    def get_all_assets():
        return list(assets_collection.find())

    @staticmethod
    def get_asset_by_id(asset_id):
        return assets_collection.find_one({"_id": ObjectId(asset_id)})

    @staticmethod
    def update_asset(asset_id, updates: dict):
        assets_collection.update_one({"_id": ObjectId(asset_id)}, {"$set": updates})

    @staticmethod
    def delete_asset(asset_id):
        assets_collection.delete_one({"_id": ObjectId(asset_id)})
        
    @staticmethod
    def get_assets_by_user(username):
        return list(assets_collection.find({"assigned_to": username}))

    @staticmethod
    def query_assets(filters: dict):
        return list(assets_collection.find(filters))