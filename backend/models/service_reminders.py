from utils.extensions import db
from datetime import date

class ServiceReminders(db.Model):
    __tablename__ = "service_reminders"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    service_type = db.Column(db.String(100), nullable=False)
    due_date = db.Column(db.Date, nullable=False)   
    note = db.Column(db.String(300), nullable=False)
    status = db.Column(db.String(20), default="pending")
    created_at = db.Column(db.Date, default=date.today)  

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "service_type": self.service_type,
            "due_date": str(self.due_date),
            "note": self.note,
            "status": self.status
        }
