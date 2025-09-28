from flask import jsonify, request, Blueprint
from apscheduler.schedulers.background import BackgroundScheduler
from models.service_reminders import ServiceReminders
from utils.extensions import db
from utils.send_email import send_email
from datetime import datetime

service_reminder_bp = Blueprint("service-reminders", __name__)
scheduler = BackgroundScheduler()
scheduler.start()


@service_reminder_bp.route("/add", methods=["POST"])
def add_reminder():
    data = request.json

    due_date = (
        datetime.strptime(data["due_date"], "%Y-%m-%d").date()
        if isinstance(data.get("due_date"), str)
        else data.get("due_date")
    )
    service_reminder = ServiceReminders(
        user_id=data["user_id"],
        service_type=data["service_type"],
        due_date=due_date,
        note=data.get("note", "")
    )

    db.session.add(service_reminder)
    db.session.commit()

    return jsonify({"message": "Reminder added successfully", "reminder": service_reminder.to_dict()})


@service_reminder_bp.route("/get/<int:user_id>", methods=["GET"])
def get_reminders(user_id):
    reminders = ServiceReminders.query.filter_by(user_id=user_id).all()
    return jsonify([r.to_dict() for r in reminders])


@service_reminder_bp.route("/service-reminder/<int:id>", methods=["PUT"])
def update_reminder(id):
    reminder = ServiceReminders.query.get_or_404(id)
    data = request.json

    reminder.service_type = data.get("service_type", reminder.service_type)
    reminder.due_date = data.get("due_date", reminder.due_date)
    reminder.note = data.get("note", reminder.note)
    reminder.status = data.get("status", reminder.status)

    db.session.commit()
    return jsonify({"message": "Reminder updated", "reminder": reminder.to_dict()})


@service_reminder_bp.route("/service-reminder/<int:id>", methods=["DELETE"])
def delete_reminder(id):
    reminder = ServiceReminders.query.get_or_404(id)
    db.session.delete(reminder)
    db.session.commit()
    return jsonify({"message": "Reminder deleted"})


@service_reminder_bp.route("/send-reminder/<int:reminder_id>", methods=["POST"])
def send_reminder(reminder_id):
    reminder = ServiceReminders.query.get_or_404(reminder_id)

    if not hasattr(reminder, "user") or not reminder.user or not reminder.user.email:
        return jsonify({"error": "User email not found"}), 400

    send_email(
        email=reminder.user.email,
        username=reminder.user.username if reminder.user.username else "User",
        service_type=reminder.service_type,
        due_date=reminder.due_date,
        note=reminder.note
    )

    reminder.status = "sent"
    db.session.commit()

    return jsonify({"message": "Reminder email sent"})


def schedule_reminder(reminder_id, due_date):
    scheduler.add_job(
        func=send_reminder,
        trigger="date",
        run_date=due_date,
        args=[reminder_id]
    )
