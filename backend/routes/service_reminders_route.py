from flask import jsonify, request, Blueprint
from models.service_reminders import ServiceReminders
from utils.extensions import db
service_reminder_bp = Blueprint("service_reminders", __name__)

@service_reminder_bp.route("/add", methods=["POST"])
def add_reminder():
    data = request.json

    service_reminder = ServiceReminders(
        user_id = data["user_id"],
        service_type = data["service_type"],
        due_date = data["due_date"],
        note = data["note",""]
    )

    db.sesstion.add(service_reminder)
    db.session.commit()

    return jsonify({"message":"Reminder added successfully!", "reminders":service_reminder.to_dict()})

@service_reminder_bp.route("/get", methods=["GET"])
def get_reminders(user_id):
    reminder = ServiceReminders.query.filter_by(user_id = user_id).all()
    return jsonify([r.to_dict() for r in reminder])


@service_reminder_bp.route("/service-reminder/<int:id>", methods=["PUT"])
def update_reminder(id):
    reminder = ServiceReminders.query.get_or_404(id)
    data = request.json

    reminder.service_type = data.get("service_type", reminder.service_type)
    reminder.due_date = data.get("due_date", reminder.due_date)
    reminder.note = data.get("note", reminder.note)
    reminder.status = data.get("status", reminder.status)

    db.session.commit()
    return jsonify({"message": "Reminder updated ✅", "reminder": reminder.to_dict()})


@service_reminder_bp.route("/service-reminder/<int:id>", methods=["DELETE"])
def delete_reminder(id):
    reminder = ServiceReminders.query.get_or_404(id)
    db.session.delete(reminder)
    db.session.commit()
    return jsonify({"message": "Reminder deleted ✅"})
