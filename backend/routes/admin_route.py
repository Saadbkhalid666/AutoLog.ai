from flask import Blueprint, request, jsonify, session
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
            # Force session creation by accessing session first
            session['user_id'] = user.id
            session.permanent = True
            
            # Then login the user
            login_user(user, remember=True, force=True, duration=timedelta(hours=24))
            
            print(f"✅ Admin logged in: {user.email}")
            print(f"📝 Session created - User ID: {user.id}, Role: {user.role}")
            print(f"🔐 Session keys: {list(session.keys())}")
            
            return jsonify({
                "message": "Admin login successful",
                "redirect": "/admin",
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "role": user.role
                }
            }), 200
        else:
            print(f"❌ Login failed for email: {email}")
            return jsonify({"error": "Invalid credentials or not admin"}), 401
    except Exception as e:
        print(f"🚨 Login error: {e}")
        return jsonify({"error": "Internal server error"}), 500

@admin_bp.route("/session-info")
def session_info():
    """Check session contents"""
    return jsonify({
        "session_keys": list(session.keys()),
        "session_data": dict(session),
        "current_user": {
            "authenticated": current_user.is_authenticated,
            "id": getattr(current_user, 'id', None),
            "email": getattr(current_user, 'email', None),
            "role": getattr(current_user, 'role', None)
        }
    }), 200
@admin_bp.route("/logout")
@login_required
def logout():
    try:
        print(f"👋 Logging out user: {current_user.email}")
        logout_user()
        return jsonify({"message": "Logout successful", "redirect": "/admin-login"}), 200
    except Exception as e:
        print(f"🚨 Logout error: {e}")
        return jsonify({"error": "Logout failed"}), 500

@admin_bp.route("/debug-auth")
def debug_auth():
    """Debug route to check authentication status"""
    try:
        debug_info = {
            "authenticated": current_user.is_authenticated,
            "user_id": getattr(current_user, 'id', None),
            "email": getattr(current_user, 'email', None),
            "role": getattr(current_user, 'role', None),
            "session_keys": list(session.keys()) if hasattr(session, 'keys') else []
        }
        print(f"🐛 DEBUG AUTH: {debug_info}")
        return jsonify(debug_info), 200
    except Exception as e:
        print(f"🚨 Debug auth error: {e}")
        return jsonify({"error": str(e)}), 500

@admin_bp.route("/test-session")
def test_session():
    """Test if session is working"""
    session['test_key'] = 'test_value'
    return jsonify({"session_set": True}), 200