from datetime import datetime
from bson import ObjectId

class Post:
    def __init__(self, title, content, author_id, created_at=None, _id=None):
        self.title = title
        self.content = content
        self.author_id = author_id
        self.created_at = created_at or datetime.utcnow()
        self._id=_id or ObjectId()

    def to_dict(self):
        return {
            '_id': str(self._id),
            'title': self.title,
            'content': self.content,
            'author_id': self.author_id,
            'created_at': self.created_at
        }
