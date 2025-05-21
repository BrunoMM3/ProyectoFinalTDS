# repositories/activo_repository.py

from repositories.mongo_cliente import get_db_connection

def obtener_activos():
    db = get_db_connection()
    return list(db.activos.find())

def insertar_activo(activo):
    db = get_db_connection()
    return db.activos.insert_one(activo)

def existe_codigo_interno(codigo):
    db = get_db_connection()
    activos_collection = db["activos"]
    return activos_collection.find_one({"codigo_interno": codigo}) is not None
