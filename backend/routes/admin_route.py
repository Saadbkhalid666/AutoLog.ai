from flask import Blueprint, request, redirect, url_for, render_template_string, current_app, session, jsonify #type:ignore
from flask_login import login_user, logout_user, login_required, current_user #type:ignore
from models.User import User
from datetime import timedelta
import traceback
from utils.extensions import db

admin_bp = Blueprint("admin_auth", __name__)

 

@admin_bp.route("/login", methods=["GET", "POST"])
def login():

    # POST (form submit)
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    user = User.query.filter_by(email=email).first()
    if user and user.check_password(password) and user.role == "admin":
        login_user(user, remember=True)

        # ensure session is permanent for the lifetime configured
        session.permanent = True
        current_app.permanent_session_lifetime = timedelta(days=7)

        return jsonify({"message": "Login successful", "redirect": "/admin"}), 200

    else:
        return "Invalid credentials or not admin", 401

@admin_bp.route("/logout")
@login_required
def logout():
    try:
        logout_user()
        return jsonify({"message": "Logout successful", "redirect": "/admin-login"}), 200
    except Exception as e:
        print(f"Logout error: {e}")
        return jsonify({"error": "Logout failed"}), 500

@admin_bp.route("/debug-auth")
def debug_auth():
    """Debug route to check authentication status"""
    try:
        return jsonify({
            "authenticated": current_user.is_authenticated,
            "user_id": getattr(current_user, 'id', None),
            "email": getattr(current_user, 'email', None),
            "role": getattr(current_user, 'role', None)
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

 