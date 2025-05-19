class User:
    def __init__(self, username, password, fullname, email, role, _id=None):
        self._id = _id
        self.username = username
        self.password = password
        self.fullname = fullname
        self.email = email
        self.role = role

    def to_dict(self):
        return {
            "username": self.username,
            "password": self.password,
            "fullname": self.fullname,
            "email": self.email,
            "role": self.role
        }
