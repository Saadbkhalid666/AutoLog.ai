from flask_mail import Message #type: ignore
from utils.extensions import mail
from config import Config
from flask import render_template_string #type: ignore
from datetime import datetime

HTML_TEMPLATE = """
<!doctype html>
<html>
  <body style="background:#0b0b0b;color:#fff;font-family:Arial;padding:20px">
    <div style="max-width:600px;margin:auto;background:#111;border-radius:12px;padding:24px">
      <h2 style="color:#00ff7f;margin:0 0 10px">AutoLog.ai — OTP Verification</h2>
      <p>Salam {{ username or "User" }},</p>
      <p>Your one-time code is:</p>
      <div style="text-align:center;margin:20px 0">
        <span style="font-size:28px;letter-spacing:6px;font-weight:bold;color:#00ff7f;
          padding:12px 24px;border:1px solid #333;border-radius:8px;display:inline-block">
          {{ otp }}
        </span>
      </div>
      <p>This code will expire in <strong>5 minutes</strong>. Do not share it with anyone.</p>
      <p style="color:#999;font-size:12px;margin-top:20px">
        &copy; {{ year }} AutoLog.ai — All rights reserved.
      </p>
    </div>
  </body>
</html>
"""

def send_otp(email, otp, username=None):
    subject = "Your AutoLog.ai OTP Code"
    sender = "AutoLog.ai"

    # Plain-text fallback
    plain_body = f"Your AutoLog.ai OTP code is: {otp}\nThis code will expire in 5 minutes."

    # Render HTML body
    html_body = render_template_string(
        HTML_TEMPLATE,
        otp=otp,
        username=username,
        year=datetime.utcnow().year
    )

    msg = Message(subject, sender=sender, recipients=[email])
    msg.body = plain_body
    msg.html = html_body

    mail.send(msg)
