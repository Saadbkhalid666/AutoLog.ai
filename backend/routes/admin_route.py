from flask import Blueprint, request, redirect, url_for, render_template_string, current_app, session, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from models.User import User
from datetime import timedelta
import traceback
from utils.extensions import db

admin_bp = Blueprint("admin_auth", __name__)

LOGIN_FORM_HTML = """
<!doctype html>
<title>Admin Login</title>
<h3>Admin Login</h3>
<form method="post">
  <input name="email" placeholder="Email" required><br>
  <input name="password" type="password" placeholder="Password" required><br>
  <button type="submit">Login</button>
</form>
"""

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

# Add this temporary route to create an admin user for testing
@admin_bp.route("/create-admin", methods=["POST"])
def create_admin():
    """Create an admin user for testing"""
    try:
        # Check if admin already exists
        existing_admin = User.query.filter_by(email="admin@autolog.com").first()
        if existing_admin:
            return jsonify({"message": "Admin user already exists", "email": "admin@autolog.com"}), 200
        
        admin_user = User(
            username="admin",
            email="admin@autolog.com", 
            role="admin"
        )
        admin_user.set_password("admin03004196455")
        
        db.session.add(admin_user)
        db.session.commit()
        
        return jsonify({
            "message": "Admin user created successfully",
            "email": "admin@autolog.com",
            "password": "admin03004196455"
        }), 201
    except Exception as e:
        print(f"Error creating admin: {e}")
        return jsonify({"error": str(e)}), 500