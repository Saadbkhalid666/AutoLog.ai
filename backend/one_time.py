# one-time script
from models.User import User
from utils.extensions import db

u = User.query.filter_by(email="saadbkhalid666@gmail.com").first()
if u:
    u.role = "admin"
    db.session.commit()
else:
    u = User(username="Admin", email="saadbkhalid666@gmail.com")
    u.set_password("123456")
    u.role = "admin"
    db.session.add(u)
    db.session.commit()
