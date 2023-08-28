# models/match.py
from datetime import datetime
from models import db  # 假设在models/__init__.py中初始化了db

class Match(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user1_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user2_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    status = db.Column(db.String(50), nullable=False)  # 可以是 'liked', 'disliked', 'matched' 等
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, user1_id, user2_id, status):
        self.user1_id = user1_id
        self.user2_id = user2_id
        self.status = status
