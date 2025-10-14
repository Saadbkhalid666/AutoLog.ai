from flask import Blueprint, request, redirect
from flask_login import login_user, logout_user, login_required
from models.User import User
from utils.extensions import csrf
from flask_wtf.csrf import generate_csrf



admin_bp = Blueprint("admin_auth",__name__)

@admin_bp.route("/login", methods=["GET", "POST"])
@csrf.exempt 
def login():
    if request.method == "POST":
        email = request.form.get("email") or request.json.get("email")
        password = request.form.get("password") or request.json.get("password")
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password) and user.role == "admin":
            login_user(user)
            return redirect("/admin") 
        else:
            return "Invalid credentials or not admin", 401

    return """
  <<form method="POST" action="/admin/login">
    <input type="hidden" name="csrf_token" value="{generate_csrf()}"/>

    <input type="email" name="email" placeholder="Email" required />
    <input type="password" name="password" placeholder="Password" required />
    <button type="submit">Login</button>
</form>
</form>

    """

    
@admin_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/admin/login")
