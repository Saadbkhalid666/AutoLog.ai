# routes/admin_auth.py
from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from models.User import User
from utils.extensions import db
from flask import current_app as app
from flask_limiter import Limiter

admin_auth = Blueprint("admin_auth", __name__, template_folder="templates")

@admin_auth.route("/admin/login", methods=["GET", "POST"])
def login():
    # Basic form handling — create a login template or accept JSON
    if request.method == "POST":
        email = request.form.get("email") or request.json.get("email")
        password = request.form.get("password") or request.json.get("password")
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password) and user.role == "admin":
            login_user(user)
            return {"message": "Logged in"}, 200
        else:
            return {"message": "Invalid credentials or not admin"}, 401

    # If GET, render a simple form (optional)
    return """
    <form method="post">
      <input name="email" placeholder="email" />
      <input name="password" type="password" placeholder="password" />
      <button type="submit">Login</button>
    </form>
    """
    
@admin_auth.route("/admin/logout")
@login_required
def logout():
    logout_user()
    return redirect("/admin/login")
