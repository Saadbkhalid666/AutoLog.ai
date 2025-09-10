from flask_mail import Message
from utils.extensions import mail
from config import Config

def send_otp(email, subject, body):
    msg = Message(
        subject,
        sender=Config.MAIL_USERNAME,
        recipients=[email]
    )
    msg.body = body
    mail.send(msg)
