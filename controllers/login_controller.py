from models.user import User
from repositories.mongo_cliente import get_db_connection
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class LoginController:
    def __init__(self):
        self.db = get_db_connection()
        self.users_collection = self.db["users"]

    def authenticate(self, username, password):
        """
        Verifica las credenciales del usuario usando MongoDB.
        """
        user_data = self.users_collection.find_one({
            "username": username,
            "password": password  # En un caso real, esto debería ser una contraseña hasheada
        })

        if user_data:
            return User(
                _id=str(user_data.get("_id")),
                username=user_data.get("username", ""),
                password=user_data.get("password", ""),
                fullname=user_data.get("fullname", ""),
                email=user_data.get("email", ""),
                role=user_data.get("role", "")
            )
        return None
