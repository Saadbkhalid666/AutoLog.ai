from flask import jsonify, request, Blueprint #type:ignore
from models.User import User

contact_bp = Blueprint("form", __name__)

@contact_bp.route("/contact", methods=['POST'])
def submit_form():
    data  = request.json
    name = data.get('name')
    email = data.get('email')
    msg = data.get('message')
    admin = User.query.filter_by()
