from flask import Blueprint, request, redirect
from flask_login import login_user, logout_user, login_required
from models.User import User

admin_bp = Blueprint("admin_auth", __name__)

@admin_bp.route("/login", methods=["GET", "POST"])
def login():
    # ✅ Disable CSRF for this specific request (if CSRFProtect is enabled globally)
    setattr(request, "_dont_enforce_csrf", True)

    if request.method == "POST":
        email = request.form.get("email") or request.json.get("email")
        password = request.form.get("password") or request.json.get("password")
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password) and user.role == "admin":
            login_user(user)
            return redirect("/admin") 
        else:
            return "Invalid credentials or not admin", 401

    # ✅ No CSRF token in form
    return """
    <form method="POST" action="/admin/login">
        <input type="email" name="email" placeholder="Email" required />
        <input type="password" name="password" placeholder="Password" required />
        <button type="submit">Login</button>
    </form>
    """

@admin_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/admin/login")
