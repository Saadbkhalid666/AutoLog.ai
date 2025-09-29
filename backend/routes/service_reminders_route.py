from flask import jsonify, request, Blueprint
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.base import ConflictingIdError
from models.service_reminders import ServiceReminders
from utils.extensions import db
from utils.send_email import send_email
from datetime import datetime, time

service_reminder_bp = Blueprint("service_reminders", __name__)

# GLOBAL scheduler (initialize only once)
scheduler = BackgroundScheduler()
if not scheduler.running:
    scheduler.start()


# ✅ INTERNAL FUNCTION (no route)
def process_reminder(reminder_id):
    reminder = ServiceReminders.query.get(reminder_id)
    if not reminder or not reminder.user or not reminder.user.email:
        return

    send_email(
        email=reminder.user.email,
        username=reminder.user.username if reminder.user.username else "User",
        service_type=reminder.service_type,
        due_date=reminder.due_date,
        note=reminder.note
    )

    reminder.status = "sent"
    db.session.commit()


def schedule_reminder(reminder_id, due_date):
    if not isinstance(due_date, datetime):
        due_date = datetime.combine(due_date, time(9))

    try:
        scheduler.add_job(
            func=process_reminder,
            trigger="date",
            run_date=due_date,
            args=[reminder_id],
            id=f"reminder_{reminder_id}",
            replace_existing=True
        )
    except ConflictingIdError:
        scheduler.remove_job(f"reminder_{reminder_id}")
        scheduler.add_job(
            func=process_reminder,
            trigger="date",
            run_date=due_date,
            args=[reminder_id],
            id=f"reminder_{reminder_id}"
        )


# ✅ ROUTES

@service_reminder_bp.route("/add", methods=["POST"])
def add_reminder():
    data = request.json

    due_date = datetime.strptime(data["due_date"], "%Y-%m-%d").date()

    reminder = ServiceReminders(
        user_id=data["user_id"],
        service_type=data["service_type"],
        due_date=due_date,
        note=data.get("note", "")
    )

    db.session.add(reminder)
    db.session.commit()

    schedule_reminder(reminder.id, due_date)

    return jsonify({"message": "Reminder added successfully", "reminder": reminder.to_dict()})


@service_reminder_bp.route("/get/<int:user_id>", methods=["GET"])
def get_reminders(user_id):
    return jsonify([r.to_dict() for r in ServiceReminders.query.filter_by(user_id=user_id).all()])


@service_reminder_bp.route("/update/<int:id>", methods=["PUT"])
def update_reminder(id):
    reminder = ServiceReminders.query.get_or_404(id)
    data = request.json
    date_updated = False

    if "due_date" in data:
        new_date = datetime.strptime(data["due_date"], "%Y-%m-%d").date()
        if new_date != reminder.due_date:
            reminder.due_date = new_date
            date_updated = True

    reminder.service_type = data.get("service_type", reminder.service_type)
    reminder.note = data.get("note", reminder.note)
    reminder.status = data.get("status", reminder.status)

    db.session.commit()
    if date_updated:
        schedule_reminder(reminder.id, reminder.due_date)

    return jsonify({"message": "Reminder updated", "reminder": reminder.to_dict()})


@service_reminder_bp.route("/delete/<int:id>", methods=["DELETE"])
def delete_reminder(id):
    reminder = ServiceReminders.query.get_or_404(id)
    db.session.delete(reminder)
    db.session.commit()

    job_id = f"reminder_{id}"
    if scheduler.get_job(job_id):
        scheduler.remove_job(job_id)

    return jsonify({"message": "Reminder deleted"})
