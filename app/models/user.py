from flask_pymongo import ObjectId

class User:
    def __init__(self, username, email, password, _id=None):
        self.username = username
        self.email = email
        self.password = password
        self._id = _id or ObjectId()

