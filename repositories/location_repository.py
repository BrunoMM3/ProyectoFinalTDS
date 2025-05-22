from repositories.mongo_cliente import get_db_connection

def guardar_ubicacion(data):
    db = get_db_connection()
    locations = db["locations"]
    locations.insert_one(data)


def obtener_ubicaciones():
    db = get_db_connection()
    return list(db.locations.find())