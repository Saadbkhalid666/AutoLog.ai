from flask import Blueprint, request, redirect, jsonify #type:ignore
from flask_login import login_user, logout_user, login_required #type:ignore
from models.User import User
from models.fuel_log import FuelLog
from models.service_reminders import ServiceReminders
from utils.extensions import db
from datetime import datetime


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

@admin_bp.route("/get-all-users", methods=["GET"])
def get_all_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users]), 200

# Update user
@admin_bp.route("/update-user/<int:id>", methods=["PUT"])
def update_user(id):
    user = User.query.get(id)
    if not user:
        return jsonify({"message": "User not found!"}), 404

    data = request.json

    if "username" in data:
        user.username = data["username"]
    if "email" in data:
        user.email = data["email"]
    if "password" in data:
        user.set_password(data["password"])
    if "role" in data:
        user.role = data["role"]

    try:
        db.session.commit()
        return jsonify({"message": "User updated successfully!", "user": user.to_dict()}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Failed to update user", "error": str(e)}), 500

# Delete user
@admin_bp.route("/del-user/<int:id>", methods=["DELETE"])
def delete_user(id):
    user = User.query.get(id)
    if not user:
        return jsonify({"message": "User not found!"}), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted successfully!"}), 200

# ------------------ Fuel Logs ------------------ #

# Get all logs
@admin_bp.route("/get-all-logs", methods=["GET"])
def get_all_logs():
    logs = FuelLog.query.all()
    return jsonify([log.to_dict() for log in logs]), 200

# Update log
@admin_bp.route("/update-log/<int:id>", methods=["PUT"])
def update_log(id):
    log = FuelLog.query.get(id)
    if not log:
        return jsonify({"message": "Fuel log not found!"}), 404

    date_str = request.json.get('date')
    date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()

    data = request.json
    log.user_id = data.get("user_id", log.user_id)
    log.litres = data.get("litres", log.litres)
    log.price = data.get("price", log.price)
    log.odometer = data.get("odometer", log.odometer)
    log.date = date_obj

    try:
        db.session.commit()
        return jsonify({"message": "Fuel log updated!", "log": log.to_dict()}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Failed to update log", "error": str(e)}), 500

# Delete log
@admin_bp.route("/del-log/<int:id>", methods=["DELETE"])
def delete_log(id):
    log = FuelLog.query.get(id)
    if not log:
        return jsonify({"message": "Fuel log not found!"}), 404
    db.session.delete(log)
    db.session.commit()
    return jsonify({"message": "Fuel log deleted!"}), 200

# ------------------ Service Reminders ------------------ #

# Get all reminders
@admin_bp.route("/get-all-reminders", methods=["GET"])
def get_all_reminders():
    reminders = ServiceReminders.query.all()
    return jsonify([r.to_dict() for r in reminders]), 200

# Update reminder
@admin_bp.route("/update-reminder/<int:id>", methods=["PUT"])
def update_reminder(id):
    reminder = ServiceReminders.query.get(id)
    if not reminder:
        return jsonify({"message": "Reminder not found!"}), 404

    data = request.json
    reminder.car_id = data.get("car_id", reminder.car_id)
    reminder.service_type = data.get("service_type", reminder.service_type)
    reminder.next_service_date = data.get("next_service_date", reminder.next_service_date)
    reminder.notes = data.get("notes", reminder.notes)

    try:
        db.session.commit()
        return jsonify({"message": "Reminder updated!", "reminder": reminder.to_dict()}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Failed to update reminder", "error": str(e)}), 500

# Delete reminder
@admin_bp.route("/del-reminder/<int:id>", methods=["DELETE"])
def delete_reminder(id):
    reminder = ServiceReminders.query.get(id)
    if not reminder:
        return jsonify({"message": "Reminder not found!"}), 404
    db.session.delete(reminder)
    db.session.commit()
    return jsonify({"message": "Reminder deleted!"}), 200