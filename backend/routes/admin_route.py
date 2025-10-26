from flask import Blueprint, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from models.User import User

admin_bp = Blueprint("admin_auth", __name__)

@admin_bp.route("/login", methods=["POST"])
def login():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
            
        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return jsonify({"error": "Email and password required"}), 400

        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password) and user.role == "admin":
            # This creates the session cookie that Flask-Admin needs
            login_user(user, remember=True)
            print(f"Admin logged in via session: {user.email}")
            
            return jsonify({
                "message": "Admin login successful",
                "redirect": "/admin"  # Redirect to Flask-Admin interface
            }), 200
        else:
            return jsonify({"error": "Invalid credentials or not admin"}), 401
    except Exception as e:
        print(f"Login error: {e}")
        return jsonify({"error": "Internal server error"}), 500

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