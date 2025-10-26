from flask import Blueprint, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from models.User import User
from datetime import timedelta
import traceback
from utils.extensions import db

admin_bp = Blueprint("admin_auth", __name__)

@admin_bp.route("/login", methods=["POST"])
def login():
    try:
        print("🔍 Login endpoint called")
        data = request.get_json()
        print(f"📦 Request data: {data}")
        
        if not data:
            return jsonify({"error": "No data provided"}), 400
            
        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return jsonify({"error": "Email and password required"}), 400

        print(f"🔐 Checking user: {email}")
        user = User.query.filter_by(email=email).first()
        print(f"👤 User found: {user is not None}")

        if user:
            print(f"🔑 Checking password and role...")
            print(f"📝 User role: {user.role}")
            password_correct = user.check_password(password)
            print(f"🔑 Password correct: {password_correct}")
            
        if user and user.check_password(password) and user.role == "admin":
            print("✅ Admin credentials verified")
            
            # Login user with Flask-Login
            login_user(user, remember=True)
            
            print(user)
            print(f"🎪 User logged in via Flask-Login: {current_user.is_authenticated}")
            
            return jsonify({
                "message": "Admin login successful",
                "redirect": "/admin"
            }), 200
        else:
            print("❌ Invalid credentials or not admin")
            return jsonify({"error": "Invalid credentials or not admin"}), 401
            
    except Exception as e:
        print(f"🚨 LOGIN ERROR: {str(e)}")
        print(f"📝 TRACEBACK: {traceback.format_exc()}")
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500

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
        admin_user.set_password("admin123")
        
        db.session.add(admin_user)
        db.session.commit()
        
        return jsonify({
            "message": "Admin user created successfully",
            "email": "admin@autolog.com",
            "password": "admin123"
        }), 201
    except Exception as e:
        print(f"Error creating admin: {e}")
        return jsonify({"error": str(e)}), 500