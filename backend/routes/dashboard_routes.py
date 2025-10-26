from flask import Blueprint, request, redirect, jsonify
from models.User import User
from models.fuel_log import FuelLog
from models.service_reminders import ServiceReminders
from utils.extensions import db
from datetime import datetime

dashboard_bp = Blueprint("dashboard", __name__)


# ---------- USER ROUTES ---------- #

@dashboard_bp.route("/get-all-users", methods=["GET"])
def get_all_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users]), 200


@dashboard_bp.route("/update-user/<int:id>", methods=["PUT"])
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


@dashboard_bp.route("/del-user/<int:id>", methods=["DELETE"])
def delete_user(id):
    user = User.query.get(id)
    if not user:
        return jsonify({"message": "User not found!"}), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted successfully!"}), 200


# ---------- FUEL LOGS ---------- #

@dashboard_bp.route("/get-all-logs", methods=["GET"])
def get_all_logs():
    logs = FuelLog.query.all()
    return jsonify([log.to_dict() for log in logs]), 200


@dashboard_bp.route("/update-log/<int:id>", methods=["PUT"])
def update_log(id):
    log = FuelLog.query.get(id)
    if not log:
        return jsonify({"message": "Fuel log not found!"}), 404

    data = request.json
    date_str = data.get("date")
    if date_str:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
        log.date = date_obj

    log.user_id = data.get("user_id", log.user_id)
    log.litres = data.get("litres", log.litres)
    log.price = data.get("price", log.price)
    log.odometer = data.get("odometer", log.odometer)

    try:
        db.session.commit()
        return jsonify({"message": "Fuel log updated!", "log": log.to_dict()}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Failed to update log", "error": str(e)}), 500


@dashboard_bp.route("/del-log/<int:id>", methods=["DELETE"])
def delete_log(id):
    log = FuelLog.query.get(id)
    if not log:
        return jsonify({"message": "Fuel log not found!"}), 404
    db.session.delete(log)
    db.session.commit()
    return jsonify({"message": "Fuel log deleted!"}), 200


# ---------- SERVICE REMINDERS ---------- #

@dashboard_bp.route("/get-all-reminders", methods=["GET"])
def get_all_reminders():
    reminders = ServiceReminders.query.all()
    return jsonify([r.to_dict() for r in reminders]), 200


@dashboard_bp.route("/update-reminder/<int:id>", methods=["PUT"])
def update_reminder(id):
    reminder = ServiceReminders.query.get(id)
    if not reminder:
        return jsonify({"message": "Reminder not found!"}), 404

    data = request.json
    reminder.user_id = data.get("user_id", reminder.user_id)
    reminder.service_type = data.get("service_type", reminder.service_type)
    date_str = data.get("due_date")
    if date_str:
        data_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
        reminder.due_date = data_obj
    reminder.note = data.get("note", reminder.note)

    try:
        db.session.commit()
        return jsonify({"message": "Reminder updated!", "reminder": reminder.to_dict()}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Failed to update reminder", "error": str(e)}), 500


@dashboard_bp.route("/del-reminder/<int:id>", methods=["DELETE"])
def delete_reminder(id):
    reminder = ServiceReminders.query.get(id)
    if not reminder:
        return jsonify({"message": "Reminder not found!"}), 404
    db.session.delete(reminder)
    db.session.commit()
    return jsonify({"message": "Reminder deleted!"}), 200
