from flask import Blueprint, request, redirect, jsonify
from flask_login import login_user, logout_user, login_required # type: ignore
from models.User import User
 

admin_bp = Blueprint("admin_auth", __name__)


@admin_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    user = User.query.filter_by(email=email).first()

    if user and user.check_password(password) and user.role == "admin":
        login_user(user, remember=True)
        print("Admin logged in ", user.email)
        return jsonify({"message": "Admin login successful"}), 200
    else:
        return jsonify({"error": "Invalid credentials or not admin"}), 401

@admin_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/admin/login")

