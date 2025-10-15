from flask import Blueprint, request, redirect, jsonify #type:ignore
from flask_login import login_user, logout_user, login_required #type:ignore
from models.User import User
from models.fuel_log import FuelLog
from models.service_reminders import ServiceReminders
admin_bp = Blueprint("admin_auth", __name__)

@admin_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email") or request.json.get("email")
        password = request.form.get("password") or request.json.get("password")
        user = User.query.filter_by(email=email).first()

        print(user.password)
        if user and user.check_password(password) and user.role == "admin":
            login_user(user)
            return redirect("/admin") 
        else:
            return "Invalid credentials or not admin", 401

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

@admin_bp.route("/get-all-users", methods=["Get"])
def get_all_users():
    users  = User.query.all()
    return jsonify([user.to_dict() for user in users]), 200    

@admin_bp.route("/get-all-logs", methods=["GET"])
def get_all_logs():
    logs = FuelLog.query.all()
    return jsonify([log.to_dict() for log in logs])

@admin_bp.route("/get-all-reminders", methods=["GET"])
def get_all_reminders():
    rem = ServiceReminders.query.all()
    return jsonify([r.to_dict() for r in rem])
