# repositories/activo_repository.py

from repositories.mongo_cliente import get_db_connection
from bson.objectid import ObjectId



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

def actualizar_activo_por_id(activo_id, nuevos_datos):
    db = get_db_connection()
    coleccion = db["activos"]
    return coleccion.update_one({"_id": ObjectId(activo_id)}, {"$set": nuevos_datos})

def obtener_activo_por_id(activo_id):
    from bson.objectid import ObjectId
    db = get_db_connection()
    coleccion = db["activos"]
    return coleccion.find_one({"_id": ObjectId(activo_id)})


def eliminar_activo_por_id(activo_id):
    db = get_db_connection()
    coleccion = db["activos"]
    return coleccion.delete_one({"_id": ObjectId(activo_id)})
