import time
from flask import Blueprint, request, jsonify #type:ignore
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity #type:ignore
from utils.extensions import db
from models.User import User
from utils.generate_otp import generate_otp
from utils.send_otp import send_otp
from datetime import timedelta
auth_bp = Blueprint("auth", __name__)
temporary_users = {}

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.json
    otp = generate_otp()
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    role = data.get("role", "user")

    if User.query.filter_by(username=username).first():
        return jsonify({"error": "Username already taken"}), 400
    if User.query.filter_by(email=email).first():
        return jsonify({"error": "User already registered"}), 400

    send_otp(email, username=username, otp=otp)
    temporary_users[otp] = {
        "username": username,
        "email": email,
        "password": password,
        "role": role,
        "otp": otp,
        "expiry": time.time() + 300
    }
    return jsonify({"message": "OTP sent successfully. Please verify to complete registration."}), 200

@auth_bp.route("/verify-otp", methods=["POST"])
def verify_otp():
    data = request.json
    otp = data.get("otp")
    storedData = temporary_users.get(otp)
    if not storedData or storedData["otp"] != otp:
        return jsonify({"message": "Invalid email or OTP"}), 400
    if time.time() > storedData["expiry"]:
        del temporary_users[otp]
        return jsonify({"message": "OTP has expired"}), 400

    user = User(
        username=storedData["username"],
        email=storedData["email"],
        password=storedData["password"],
        role=storedData["role"],
    )
    db.session.add(user)
    db.session.commit()
    del temporary_users[otp]

    access_token = create_access_token(identity=str(user.id), expires_delta=timedelta(days=7))
    return jsonify({
        "message": "OTP verified and user created successfully!",
        "username": user.username,
        "email": user.email,
        "token": access_token,
        "role":user.role
    }), 201

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    if not data:
        return jsonify({"message": "No data provided"}), 400
    email = data.get("email")
    password = data.get("password")
    if not email or not password:
        return jsonify({"message": "Email and password required"}), 400

    user = User.query.filter_by(email=email).first()
    if not user or user.password != password:
        return jsonify({"message": "Invalid email or password!"}), 401

    access_token = create_access_token(identity=str(user.id), expires_delta=timedelta(days=7))
    return jsonify({
        "message": "Login successful!",
        "username": user.username,
        "email": user.email,
        "user_id": user.id,
        "token": access_token,
        "role":user.role
    }), 200

 