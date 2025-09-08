from flask import Blueprint, request, jsonify
from utils.db import db
from models.User import User

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.json
    user = User(
        username=data["username"],
        email=data["email"],
        password=data["password"],
        role=data.get("role", "user")
    )
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "User registered successfully!"})

