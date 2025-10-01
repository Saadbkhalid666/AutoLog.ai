# routes/service_reminders_route.py
import logging
from flask import jsonify, request, Blueprint, current_app #type:ignore 
from models.service_reminders import ServiceReminders
from models.User import User
from utils.extensions import db
from utils.send_email import send_email
from datetime import datetime, time, timedelta, date

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

service_reminder_bp = Blueprint("service-reminders", __name__)

# Valid status values
VALID_STATUSES = {"pending", "sent", "cancelled"}

def process_reminder(app, reminder_id):
    with app.app_context():
        logger.info(f"Running reminder job for ID: {reminder_id}")
        reminder = ServiceReminders.query.get(reminder_id)
        if not reminder or not reminder.user or not reminder.user.email:
            logger.warning(f"Reminder {reminder_id} skipped: No email or user found")
            return

        try:
            # Convert due_date to string for send_email
            due_date_str = reminder.due_date.strftime("%Y-%m-%d")
            send_email(
                email=reminder.user.email,
                username=reminder.user.username or "User",
                service_type=reminder.service_type,
                due_date=due_date_str,  # Pass as string
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

@service_reminder_bp.route("/test-reminder/<int:id>", methods=["GET"])
def test_reminder(id):
    reminder = ServiceReminders.query.get(id)
    if not reminder:
        logger.warning(f"Test reminder failed: Reminder ID {id} not found")
        return jsonify({"error": f"Reminder with ID {id} not found"}), 404
    if not reminder.user:
        logger.warning(f"Test reminder failed: No user for reminder ID {id}")
        return jsonify({"error": f"No user associated with reminder ID {id}"}), 404
    schedule_reminder(id, None, test_mode=True)
    logger.info(f"Test reminder scheduled for ID {id}")
    return jsonify({"message": f"Test reminder scheduled for ID {id}"})

@service_reminder_bp.route("/add", methods=["POST"])
def add_reminder():
    data = request.json
    try:
        due_date = datetime.strptime(data["due_date"], "%Y-%m-%d").date()
    except (KeyError, ValueError):
        logger.warning(f"Add reminder failed: Invalid due_date format")
        return jsonify({"error": "Invalid or missing due_date (format: YYYY-MM-DD)"}), 400

    if not data.get("user_id") or not data.get("service_type") or not data.get("note"):
        logger.warning(f"Add reminder failed: Missing required fields")
        return jsonify({"error": "user_id, service_type, and note are required"}), 400

    if len(data["service_type"]) > 100 or len(data["note"]) > 300:
        logger.warning(f"Add reminder failed: service_type or note too long")
        return jsonify({"error": "service_type (max 100 chars) or note (max 300 chars) too long"}), 400

    user = User.query.get(data["user_id"])
    if not user:
        logger.warning(f"Add reminder failed: User ID {data['user_id']} not found")
        return jsonify({"error": f"User with ID {data['user_id']} not found"}), 404

    try:
        reminder = ServiceReminders(
            user_id=data["user_id"],
            service_type=data["service_type"],
            due_date=due_date,
            note=data["note"],
            status="pending",
            created_at=date.today()
        )
        db.session.add(reminder)
        db.session.commit()
        schedule_reminder(reminder.id, due_date)
        logger.info(f"Reminder {reminder.id} added for user {data['user_id']}")
        return jsonify({"message": "Reminder added", "reminder": reminder.to_dict()}), 201
    except Exception as e:
        db.session.rollback()
        logger.error(f"Failed to add reminder: {str(e)}")
        return jsonify({"error": "Failed to add reminder"}), 500

@service_reminder_bp.route("/get/<int:user_id>", methods=["GET"])
def get_reminders(user_id):
    user = User.query.get(user_id)
    if not user:
        logger.warning(f"Get reminders failed: User ID {user_id} not found")
        return jsonify({"error": f"User with ID {user_id} not found"}), 404
    reminders = ServiceReminders.query.filter_by(user_id=user_id).all()
    logger.info(f"Retrieved {len(reminders)} reminders for user {user_id}")
    return jsonify([r.to_dict() for r in reminders])

@service_reminder_bp.route("/update/<int:id>", methods=["PUT"])
def update_reminder(id):
    reminder = ServiceReminders.query.get_or_404(id)
    data = request.json
    if "due_date" in data:
        try:
            new_date = datetime.strptime(data["due_date"], "%Y-%m-%d").date()
            if new_date != reminder.due_date:
                reminder.due_date = new_date
                schedule_reminder(reminder.id, new_date)
        except ValueError:
            logger.warning(f"Update reminder {id} failed: Invalid due_date format")
            return jsonify({"error": "Invalid due_date format (YYYY-MM-DD)"}), 400

    reminder.service_type = data.get("service_type", reminder.service_type)
    reminder.note = data.get("note", reminder.note)
    reminder.status = data.get("status", reminder.status)

    if not reminder.service_type or not reminder.note:
        logger.warning(f"Update reminder {id} failed: service_type or note empty")
        return jsonify({"error": "service_type and note cannot be empty"}), 400
    if len(reminder.service_type) > 100 or len(reminder.note) > 300:
        logger.warning(f"Update reminder {id} failed: service_type or note too long")
        return jsonify({"error": "service_type (max 100 chars) or note (max 300 chars) too long"}), 400
    if reminder.status not in VALID_STATUSES:
        logger.warning(f"Update reminder {id} failed: Invalid status {reminder.status}")
        return jsonify({"error": f"status must be one of {VALID_STATUSES}"}), 400

    try:
        db.session.commit()
        logger.info(f"Reminder {id} updated")
        return jsonify({"message": "Reminder updated", "reminder": reminder.to_dict()})
    except Exception as e:
        db.session.rollback()
        logger.error(f"Failed to update reminder {id}: {str(e)}")
        return jsonify({"error": "Failed to update reminder"}), 500

@service_reminder_bp.route("/delete/<int:id>", methods=["DELETE"])
def delete_reminder(id):
    reminder = ServiceReminders.query.get_or_404(id)
    job_id = f"reminder_{id}"
    scheduler = current_app.scheduler
    try:
        db.session.delete(reminder)
        db.session.commit()
        if scheduler.get_job(job_id):
            scheduler.remove_job(job_id)
            logger.info(f"Removed scheduler job {job_id}")
        logger.info(f"Reminder {id} deleted")
        return jsonify({"message": "Reminder deleted"})
    except Exception as e:
        db.session.rollback()
        logger.error(f"Failed to delete reminder {id}: {str(e)}")
        return jsonify({"error": "Failed to delete reminder"}), 500