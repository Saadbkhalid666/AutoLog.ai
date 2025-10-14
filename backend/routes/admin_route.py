from flask import Blueprint, request, redirect
from flask_login import login_user, logout_user, login_required
from models.User import User

admin_auth = Blueprint("admin_auth", __name__, url_prefix="/admin")

@admin_auth.route("/login", methods=["GET", "POST"])
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
