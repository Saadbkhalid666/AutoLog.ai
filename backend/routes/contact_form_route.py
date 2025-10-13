from flask import jsonify, request, Blueprint #type:ignore
from models.User import User
from utils.contact_mail import send_email

contact_bp = Blueprint("form", __name__)

@contact_bp.route("/contact", methods=['POST'])
def submit_form():
    data  = request.json
    name = data.get('name')
    email = data.get('email')
    msg = data.get('message')
    admin = User.query.filter_by(role="admin").first()
    admin_email = admin.email if email else None

    send_email(name,email,msg,admin_email)
    return jsonify({"message":"Form submitted!"}), 200
