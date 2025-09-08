from flask import Blueprint, jsonify
from flask_mail import Message
from app import mail
from config import Config
from generate_otp import generate_otp

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/send-otp", methods=["POST"])
def send_otp():
    subject = "Your OTP Code"
    body = f"Your OTP code is {generate_otp()}"

    msg = Message(
        subject,
        sender=Config.MAIL_USERNAME,
        recipients=["receiver@gmail.com"]  
    )
    msg.body = body

    mail.send(msg)
    return jsonify({"message": "OTP sent successfully!"})
