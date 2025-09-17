import os
from flask import render_template_string
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from datetime import datetime
from dotenv import load_dotenv

# Load .env variables
load_dotenv()

# Environment variables
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
VERIFIED_EMAIL = os.getenv("VERIFIED_EMAIL")

# HTML template
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
    """
    Sends OTP email using SendGrid
    """
    if not SENDGRID_API_KEY or not VERIFIED_EMAIL:
        raise ValueError("SendGrid API key or verified email not set in .env")

    subject = "Your AutoLog.ai OTP Code"

    # Plain text fallback
    plain_body = f"Your AutoLog.ai OTP code is: {otp}\nThis code will expire in 5 minutes."

    # Render HTML body
    html_body = render_template_string(
        HTML_TEMPLATE,
        otp=otp,
        username=username,
        year=datetime.utcnow().year
    )

    # Build SendGrid Mail object
    message = Mail(
        from_email=VERIFIED_EMAIL,
        to_emails=email,
        subject=subject,
        plain_text_content=plain_body,
        html_content=html_body
    )

    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        print(f"✅ OTP email sent! Status: {response.status_code}")
    except Exception as e:
        print(f"❌ Error sending email: {e}")
