from models.user import User
from repositories.mongo_cliente import get_db_connection
from pymongo.errors import DuplicateKeyError

class RegisterController:
    def __init__(self):
        self.db = get_db_connection()
        self.users_collection = self.db["users"]

    def register_user(self, username, password, fullname, email, role):
        # Validaciones básicas
        if self.users_collection.find_one({"username": username}):
            return False, "El nombre de usuario ya está en uso."

        new_user = User(username, password, fullname, email, role="usuario")
        try:
            self.users_collection.insert_one(new_user.to_dict())
            return True, "Registro exitoso."
        except DuplicateKeyError:
            return False, "El usuario ya existe."
        except Exception as e:
            return False, f"Error al registrar: {str(e)}"
