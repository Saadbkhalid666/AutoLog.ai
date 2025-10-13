from flask_mail import Message 
from flask import render_template_string
from configuration.config import Config
from datetime import datetime
from utils.extensions import mail
import pytz

PK_TZ = pytz.timezone("Asia/Karachi")

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


CONTACT_FORM_TEMPLATE = """
<!doctype html>
<html>
  <body style="background:#0b0b0b;color:#fff;font-family:Arial,Helvetica,sans-serif;padding:20px">
    <div style="max-width:600px;margin:auto;background:#111;border-radius:12px;padding:24px;box-shadow:0 0 24px rgba(0,255,127,0.08)">
      <h2 style="color:#00ff7f;margin:0 0 10px">📩 New Contact Form Submission — AutoLog.ai</h2>
      
      <p style="color:white;">Hi Admin,</p>
      <p style="color:white;">You have received a new message from your website contact form:</p>

      <div style="background:#000;border:1px solid #1f1f1f;padding:16px;border-radius:10px;margin:20px 0">
        <p style="margin:6px 0"><strong style="color:#bfbfbf">Name:</strong> <span style="color:#e8e8e8">{{ user_name }}</span></p>
        <p style="margin:6px 0"><strong style="color:#bfbfbf">Email:</strong> <span style="color:#e8e8e8">{{ user_email }}</span></p>
        <p style="margin:6px 0"><strong style="color:#bfbfbf">Message:</strong></p>
        <p style="margin:6px 0;color:#e8e8e8">{{ user_message }}</p>
      </div>

      <p style="margin-top:30px;color:#7a7a7a;font-size:12px">~ AutoLog.ai System<br>📎 Sent via www.autolog.ai/contact</p>
    </div>
  </body>
</html>
"""

def send_email(user_name,user_email, user_message, admin_mail):
    subject = "New Contact Form Submission"
    sender = Config.MAIL_USERNAME

    html_body = render_template_string(
        CONTACT_FORM_TEMPLATE,
        user_name=user_name,
        user_email=user_email,
        user_message=user_message
        
    )
    msg = Message(subject, sender=sender , recipients=[admin_mail])
    msg.html = html_body
    mail.send(msg)
    