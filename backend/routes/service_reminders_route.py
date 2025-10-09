import logging
from flask import jsonify, request, Blueprint, current_app #type:ignore
from flask_jwt_extended import jwt_required, get_jwt_identity #type:ignore
from models.service_reminders import ServiceReminders
from models.User import User
from utils.extensions import db
from utils.send_email import send_email
from datetime import datetime, time, timedelta, date

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

service_reminder_bp = Blueprint("service-reminders", __name__)
VALID_STATUSES = {"pending", "sent", "cancelled"}

def process_reminder(app, reminder_id):
    with app.app_context():
        logger.info(f"Running reminder job for ID: {reminder_id}")
        reminder = ServiceReminders.query.get(reminder_id)
        if not reminder or not reminder.user or not reminder.user.email:
            logger.warning(f"Reminder {reminder_id} skipped: No email or user found")
            return
        try:
            due_date_str = reminder.due_date.strftime("%Y-%m-%d")
            send_email(
                email=reminder.user.email,
                username=reminder.user.username or "User",
                service_type=reminder.service_type,
                due_date=due_date_str,
                note=reminder.note
            )
            reminder.status = "sent"
            db.session.commit()
            logger.info(f"Email sent & status updated for reminder {reminder_id}")
        except Exception as e:
            logger.error(f"Failed to process reminder {reminder_id}: {str(e)}")
            db.session.rollback()

def schedule_reminder(reminder_id, due_date, test_mode=False):
    app = current_app._get_current_object()
    scheduler = app.scheduler
    if test_mode:
        due_date = datetime.now() + timedelta(seconds=20)
    else:
        if not isinstance(due_date, datetime):
            due_date = datetime.combine(due_date, time(9, 0))
    job_id = f"reminder_{reminder_id}"
    try:
        scheduler.add_job(
            func=process_reminder,
            trigger="date",
            run_date=due_date,
            args=[app, reminder_id],
            id=job_id,
            replace_existing=True
        )
        logger.info(f"Scheduled reminder job {job_id} for {due_date}")
    except Exception as e:
        logger.error(f"Failed to schedule reminder {reminder_id}: {str(e)}")

@service_reminder_bp.route("/add", methods=["POST"])
@jwt_required()
def add_reminder():
    user_id = get_jwt_identity()
    data = request.json
    try:
        due_date = datetime.strptime(data["due_date"], "%Y-%m-%d").date()
    except (KeyError, ValueError):
        return jsonify({"error": "Invalid or missing due_date (format: YYYY-MM-DD)"}), 400

    service_type = data.get("service_type")
    note = data.get("note")
    if not service_type or not note:
        return jsonify({"error": "service_type and note are required"}), 400
    if len(service_type) > 100 or len(note) > 300:
        return jsonify({"error": "service_type (max 100 chars) or note (max 300 chars) too long"}), 400

    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    try:
        reminder = ServiceReminders(
            user_id=user_id,
            service_type=service_type,
            due_date=due_date,
            note=note,
            status="pending",
            created_at=date.today()
        )
        db.session.add(reminder)
        db.session.commit()
        schedule_reminder(reminder.id, due_date)
        return jsonify({"message": "Reminder added", "reminder": reminder.to_dict()}), 201
    except Exception:
        db.session.rollback()
        return jsonify({"error": "Failed to add reminder"}), 500

@service_reminder_bp.route("/get", methods=["GET"])
@jwt_required()
def get_reminders():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    reminders = ServiceReminders.query.filter_by(user_id=user_id).all()
    return jsonify([r.to_dict() for r in reminders])

@service_reminder_bp.route("/update/<int:id>", methods=["PUT"])
@jwt_required()
def update_reminder(id):
    user_id = get_jwt_identity()
    reminder = ServiceReminders.query.get_or_404(id)
    if reminder.user_id != user_id:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.json
    if "due_date" in data:
        try:
            new_date = datetime.strptime(data["due_date"], "%Y-%m-%d").date()
            if new_date != reminder.due_date:
                reminder.due_date = new_date
                schedule_reminder(reminder.id, new_date)
        except ValueError:
            return jsonify({"error": "Invalid due_date format (YYYY-MM-DD)"}), 400

    reminder.service_type = data.get("service_type", reminder.service_type)
    reminder.note = data.get("note", reminder.note)
    reminder.status = data.get("status", reminder.status)

    if not reminder.service_type or not reminder.note:
        return jsonify({"error": "service_type and note cannot be empty"}), 400
    if len(reminder.service_type) > 100 or len(reminder.note) > 300:
        return jsonify({"error": "service_type (max 100 chars) or note (max 300 chars) too long"}), 400
    if reminder.status not in VALID_STATUSES:
        return jsonify({"error": f"status must be one of {VALID_STATUSES}"}), 400

    try:
        db.session.commit()
        return jsonify({"message": "Reminder updated", "reminder": reminder.to_dict()})
    except Exception:
        db.session.rollback()
        return jsonify({"error": "Failed to update reminder"}), 500

@service_reminder_bp.route("/delete/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_reminder(id):
    user_id = get_jwt_identity()
    reminder = ServiceReminders.query.get_or_404(id)
    if reminder.user_id != user_id:
        return jsonify({"error": "Unauthorized"}), 401

    job_id = f"reminder_{id}"
    scheduler = current_app.scheduler
    try:
        db.session.delete(reminder)
        db.session.commit()
        if scheduler.get_job(job_id):
            scheduler.remove_job(job_id)
        return jsonify({"message": "Reminder deleted"})
    except Exception:
        db.session.rollback()
        return jsonify({"error": "Failed to delete reminder"}), 500
