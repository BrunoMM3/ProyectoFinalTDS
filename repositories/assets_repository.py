from bson.objectid import ObjectId
from bcrypt import hashpw, gensalt
from repositories.mongo_cliente import get_db_connection
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Obtener la base de datos
try:
    db = get_db_connection()
    logger.info("Conexión a la base de datos establecida")
except Exception as e:
    logger.error(f"Error al conectar a la base de datos: {str(e)}")
    raise

# Colecciones
users_collection = db["users"]
assets_collection = db["activos"]
maintenances_collection = db["maintenances"]
locations_collection = db["locations"]
assignments_collection = db["assignments"]
config_collection = db["config"]

def create_indexes():
    try:
        users_collection.create_index("username", unique=True)
        assets_collection.create_index("serial_number", unique=True)
        logger.info("Índices creados correctamente")
    except Exception as e:
        logger.error(f"Error al crear índices: {str(e)}")
        raise

def insert_sample_admin():
    try:
        if users_collection.count_documents({"username": "admin"}) == 0:
            hashed = hashpw("admin123".encode('utf-8'), gensalt())
            superadmin_hashed = hashpw("superadmin123".encode('utf-8'), gensalt())
            users_collection.insert_one({
                "username": "admin",
                "password": hashed,
                "fullname": "Administrador General",
                "email": "admin@empresa.com",
                "role": "admin",
                "superadmin_password": superadmin_hashed
            })
            logger.info("Usuario admin creado correctamente")
        else:
            logger.info("Usuario admin ya existe")
    except Exception as e:
        logger.error(f"Error al insertar usuario admin: {str(e)}")
        raise

def get_superadmin_password():
    try:
        admin = users_collection.find_one({"username": "admin"})
        if admin and "superadmin_password" in admin:
            logger.info("Contraseña de superadministrador encontrada")
            return admin["superadmin_password"]
        logger.error("Contraseña de superadministrador no encontrada")
        return None
    except Exception as e:
        logger.error(f"Error al obtener contraseña de superadministrador: {str(e)}")
        return None

if __name__ == "__main__":
    try:
        create_indexes()
        insert_sample_admin()
        print("Base de datos inicializada.")
    except Exception as e:
        print(f"Error al inicializar la base de datos: {str(e)}")