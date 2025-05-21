from repositories.mongo_cliente import get_db_connection
from models.user import User
from utils.hash_utils import check_password

class LoginController:
    def __init__(self):
        self.db = get_db_connection()
        self.users_collection = self.db["users"]

    def login_user(self, username, password):
        user_data = self.users_collection.find_one({"username": username})
        if user_data:
            hashed_password = user_data.get("password")
            if check_password(password, hashed_password):
                return User(
                    _id=user_data["_id"],
                    username=user_data["username"],
                    password=hashed_password,
                    fullname=user_data["fullname"],
                    email=user_data["email"],
                    role=user_data["role"]
                )
        return None
