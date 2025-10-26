# models/user.py
from datetime import datetime
from utils.extensions import db
from flask_login import UserMixin #type:ignore
from werkzeug.security import generate_password_hash, check_password_hash #type:ignore


class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(50), nullable=False, default='user')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    def to_dict(self):
       return {
            "id": self.id,
            "username":self.username,
            "email":self.email,
            "password":self.password,
            "role":self.role,
            "created_at":self.created_at.isoformat()
        }
