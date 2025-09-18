import time
from flask import Blueprint, request, jsonify # type: ignore
from utils.extensions import db
from models.User import User # type: ignore
from utils.generate_otp import generate_otp
from utils.send_otp import send_otp

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

    # Check if username already exists
    if User.query.filter_by(username=username).first():
        return jsonify({"error": "Username already taken"}), 400

    # Check if email already exists
    if User.query.filter_by(email=email).first():
        return jsonify({"error": "User already registered"}), 400

    # Send OTP email
    send_otp(email, username=username, otp=otp)

    # Store temporary user data
    temporary_users[otp] = {
        "username": username,
        "email": email,
        "password": password,
        "role": role,
        "otp": otp,
        "expiry": time.time() + 300  # 5 minutes
    }

    # ✅ Only message here, no username
    return jsonify({"message": "OTP sent successfully. Please verify to complete registration."}), 200


@auth_bp.route("/verify-otp", methods=["POST"])
def verify_otp():
    data = request.json
    otp = data.get("otp")

    storedData = temporary_users.get(otp)
    if not storedData:
        return jsonify({"message": "Invalid email or OTP"}), 400

    if storedData["otp"] != otp:
        return jsonify({"message": "Invalid email or OTP"}), 400

    if time.time() > storedData["expiry"]:
        del temporary_users[otp]
        return jsonify({"message": "OTP has expired"}), 400

    # Create new user
    user = User(
        username=storedData["username"],
        email=storedData["email"],
        password=storedData["password"],  # ⚠️ hash password later
        role=storedData["role"],
    )
    db.session.add(user)
    db.session.commit()

    del temporary_users[otp]

    # ✅ Return username + email so Angular can save it
    return jsonify({
        "message": "OTP verified and user created successfully!",
        "username": user.username,
        "email": user.email
    }), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    user = User.query.filter_by(email=email, password=password).first()
    if user:
        # ✅ Return username + email
        return jsonify({
            "message": "Login successful!",
            "username": user.username,
            "email": user.email
        }), 200
    else:
        return jsonify({"message": "User not found!"}), 404
