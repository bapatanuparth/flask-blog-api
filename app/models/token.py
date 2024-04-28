from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import datetime
from app.extensions import mongo


class Token:
    def __init__(self, user_id, token, expires):
        self.user_id = ObjectId(user_id) 
        self.token = token
        self.expires = expires 

    def save(self):
        """Save the token into the MongoDB database."""
        token_data = {
            'user_id': self.user_id,
            'token': self.token,
            'expires': self.expires,
            'created_at': datetime.datetime.utcnow()
        }
        return mongo.db.tokens.insert_one(token_data)

    @staticmethod
    def find_by_token(token_str):
        """Find a token document in the database."""
        return mongo.db.tokens.find_one({'token': token_str})

    @staticmethod
    def delete(token_str):
        """Delete a token from the database."""
        return mongo.db.tokens.delete_one({'token': token_str})
