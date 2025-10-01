from flask_mail import Message #type:ignore
from flask import render_template_string #type:ignore
from configuration.config import Config
from utils.extensions import mail
from datetime import datetime
import pytz #type:ignore

PK_TZ = pytz.timezone("Asia/Karachi")

# ---- Helpers ----
def _to_datetime(value):
    if isinstance(value, datetime):
        dt = value
    else:
        try:
            dt = datetime.fromisoformat(value)
        except Exception:
            dt = datetime.strptime(value, "%Y-%m-%d")
    if dt.tzinfo is None:
        dt = PK_TZ.localize(dt)
    else:
        dt = dt.astimezone(PK_TZ)
    return dt

def _format_date_readable(value):
    dt = _to_datetime(value)
    return dt.strftime("%d %B %Y")  # e.g. 23 October 2025


# ---- SERVICE REMINDER TEMPLATE (Dark Neon Style) ----
SERVICE_REMINDER_TEMPLATE = """
<!doctype html>
<html>
  <body style="background:#0b0b0b;color:#fff;font-family:Arial,Helvetica,sans-serif;padding:20px">
    <div style="max-width:600px;margin:auto;background:#111;border-radius:12px;padding:24px;box-shadow:0 0 24px rgba(0,255,127,0.08)">
      <h2 style="color:#00ff7f;margin:0 0 10px">AutoLog.ai — Service Reminder</h2>
      <p style="color:white;">Salam {{ username or "User" }},</p>
      <p style="color:white;">This is a friendly reminder for your upcoming vehicle service:</p>
      <div style="background:#000;border:1px solid #1f1f1f;padding:16px;border-radius:10px;margin:20px 0">
        <p style="margin:6px 0"><strong style="color:#bfbfbf">Service Type:</strong> <span style="color:#e8e8e8">{{ service_type }}</span></p>
        <p style="margin:6px 0"><strong style="color:#bfbfbf">Due Date:</strong> <span style="color:#e8e8e8">{{ due_date_readable }}</span></p>
        {% if note %}
        <p style="margin:6px 0"><strong style="color:#bfbfbf">Note:</strong> <span style="color:#e8e8e8">{{ note }}</span></p>
        {% endif %}
      </div>
      <p style="color:white;">Stay safe on the road 🚗💨</p>
      <p style="margin-top:30px;color:#7a7a7a;font-size:12px">~ AutoLog.ai System</p>
    </div>
  </body>
</html>
"""

# ---- Public Function ----
def send_email(email, username, service_type, due_date, note=None):
    subject = "Your AutoLog.ai Service Reminder"
    sender = Config.MAIL_USERNAME

    html_body = render_template_string(
        SERVICE_REMINDER_TEMPLATE,
        username=username,
        service_type=service_type,
        due_date_readable=_format_date_readable(due_date),
        note=note or ""
    )

    msg = Message(subject, sender=sender, recipients=[email])
    msg.html = html_body
    mail.send(msg)
