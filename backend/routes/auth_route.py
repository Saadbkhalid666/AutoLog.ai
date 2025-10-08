import time
from flask import Blueprint, request, jsonify, session # type: ignore

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
        password=storedData["password"],  
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
    try:
        data = request.json
        if not data:
            return jsonify({"message": "No data provided"}), 400
            
        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return jsonify({"message": "Email and password required"}), 400

        print(f"Login attempt for email: {email}")

        user = User.query.filter_by(email=email).first()
        if not user:
            print("User not found")
            return jsonify({"message": "Invalid email or password!"}), 401
            
        # Check password (consider hashing passwords in future)
        if user.password != password:
            print("Password mismatch")
            return jsonify({"message": "Invalid email or password!"}), 401

        # Clear and create new session
        session.clear()
        session["user_id"] = user.id
        session["username"] = user.username
        session.modified = True
        
        print(f"✅ Login successful - user_id: {session.get('user_id')}, username: {session.get('username')}")
        
        return jsonify({
            "message": "Login successful!",
            "username": user.username,
            "email": user.email,
            "user_id": user.id
        }), 200
        
    except Exception as e:
        print(f"Login error: {str(e)}")
        return jsonify({"message": "Server error during login"}), 500

@auth_bp.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return jsonify({"message": "Logged out successfully!"}), 200


@auth_bp.route("/check-session", methods=["GET"])
def check_session():
    user_id = session.get("user_id")
    username = session.get("username")
    return jsonify({
        "user_id": user_id,
        "username": username,
        "session_keys": list(session.keys()),
        "message": "Session check successful"
    }), 200

 