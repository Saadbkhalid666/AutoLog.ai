import os
import pytesseract #type:ignore
from flask import Blueprint, request, jsonify #type:ignore
from flask_jwt_extended import jwt_required, get_jwt_identity #type:ignore
from utils.extensions import db
from models.fuel_log import FuelLog
from datetime import datetime
from PIL import Image #type:ignore

fuel_log_bp = Blueprint("vehicle", __name__)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
@fuel_log_bp.route("/fuel-log/manual", methods=["POST"])
@jwt_required()
def post_manual_fuel_log():
    user_id = get_jwt_identity()
    data = request.get_json()
    date_value = data.get("date")
    if date_value:
        date_value = datetime.fromisoformat(date_value).date()
    else:
        date_value = datetime.utcnow().date()

    try:
        litres = float(data.get("litres", 0))
        price = float(data.get("price", 0))
        odometer = int(data.get("odometer", 0))
    except ValueError:
        return jsonify({"error": "Invalid number format"}), 422

    fuel_log = FuelLog(
        user_id=user_id,
        date=date_value,
        litres=litres,
        price=price,
        odometer=odometer
    )

    db.session.add(fuel_log)
    db.session.commit()

    return jsonify({
        "message": "Fuel log created successfully",
        "fuel_log": fuel_log.to_dict()
    }), 201

@fuel_log_bp.route("/fuel-logs/ocr", methods=["POST"])
@jwt_required()
def post_ocr_fuel_log():
    user_id = get_jwt_identity()
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded!"}), 400
    
    file = request.files["file"]
    filepath = os.path.join("uploads", file.filename)
    file.save(filepath)

    img = Image.open(filepath)
    text = pytesseract.image_to_string(img)

    litres = "50"
    price = "4000"
    odometer = "12345"
    date = datetime.utcnow().date()

    fuel_log = FuelLog(
    user_id=user_id,
    date=date,
    litres=float(litres),
    price=float(price),
    odometer=int(odometer)
)

    db.session.add(fuel_log)
    db.session.commit()

    return jsonify({
        "extracted_text": text,
        "fuel_log": {
            "date": date,
            "litres": litres,
            "price": price,
            "odometer": odometer
        }
    })

@fuel_log_bp.route("/get-fuel-logs", methods=["GET"])
@jwt_required()
def get_fuel_logs():
    user_id = get_jwt_identity()
    logs = FuelLog.query.filter_by(user_id=user_id).order_by(FuelLog.date.desc()).all()
    logs_list = [log.to_dict() for log in logs]
    return jsonify({"fuel_logs": logs_list})

@fuel_log_bp.route("/update-fuel-log/<int:log_id>", methods=["PUT"])
@jwt_required()
def update_fuel_log_by_id(log_id):
    user_id = get_jwt_identity()
    log = FuelLog.query.get(log_id)
    if not log or log.user_id != user_id:
        return jsonify({"error": "Fuel Log not found or unauthorized!"}), 404

    data = request.get_json()
    log.date = datetime.utcnow().date()
    log.litres = data.get("litres", log.litres)
    log.price = data.get("price", log.price)
    log.odometer = data.get("odometer", log.odometer)

    db.session.commit()
    return jsonify({"message": "Fuel log updated!", "fuel_log": log.to_dict()})

@fuel_log_bp.route("/delete-fuel-log/<int:log_id>", methods=["DELETE"])
@jwt_required()
def delete_fuel_log(log_id):
    user_id = get_jwt_identity()
    log = FuelLog.query.get(log_id)
    if not log or log.user_id != user_id:
        return jsonify({"error": "Fuel Log not found or unauthorized!"}), 404

    db.session.delete(log)
    db.session.commit()
    return jsonify({"message": "Fuel log deleted successfully!"}), 200
