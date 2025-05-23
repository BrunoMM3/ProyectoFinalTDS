from models.user import User
from repositories.mongo_cliente import get_db_connection
from pymongo.errors import DuplicateKeyError
from utils.hash_utils import hash_password  # Importar
import re
class RegisterController:
    def __init__(self):
        self.db = get_db_connection()
        self.users_collection = self.db["users"]

    def register_user(self, username, password, fullname, email, role):
        # Validaciones de campos
        if not username or len(username) < 3:
            return False, "El nombre de usuario debe tener al menos 3 caracteres."
        if not password or len(password) < 6:
            return False, "La contraseña debe tener al menos 6 caracteres."
        if not fullname:
            return False, "El nombre completo es obligatorio."
        if not email or not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return False, "El correo electrónico no es válido."

        if self.users_collection.find_one({"username": username}):
            return False, "El nombre de usuario ya está en uso."

        hashed_password = hash_password(password)  # Aquí encriptamos la contraseña
        new_user = User(username, hashed_password, fullname, email, role)
        
        try:
            self.users_collection.insert_one(new_user.to_dict())
            return True, "Registro exitoso."
        except DuplicateKeyError:
            return False, "El usuario ya existe."
        except Exception as e:
            return False, f"Error al registrar: {str(e)}"