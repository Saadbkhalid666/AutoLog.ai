import os
import pytesseract #type:ignore
from flask import Blueprint, request, jsonify, session #type:ignore
from utils.extensions import db
from models.fuel_log import FuelLog
from datetime import datetime
from PIL import Image #type:ignore

fuel_log_bp = Blueprint("vehicle", __name__)

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


@fuel_log_bp.route("/fuel-log/manual", methods=["POST"])
def post_manual_fuel_log():
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "Unauthorized!"}), 401

    data = request.get_json()
    date_value = data.get("date")
    if date_value:
        date_value = datetime.fromisoformat(date_value).date()
    else:
        date_value = datetime.utcnow().date()

    fuel_log = FuelLog(
        user_id=user_id,
        date=date_value,
        litres=data.get("litres"),
        price=data.get("price"),
        odometer=data.get("odometer")
    )

    db.session.add(fuel_log)
    db.session.commit()

    return jsonify({
        "message": "Fuel log created successfully",
        "fuel_log": fuel_log.to_dict()
    }), 201


@fuel_log_bp.route("/fuel-logs/ocr", methods=["POST"])
def post_ocr_fuel_log():
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "Unauthorized!"}), 401

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
        litres=litres,
        price=price,
        odometer=odometer
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
def get_fuel_logs():
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "Unauthorized!"}), 401

    logs = FuelLog.query.filter_by(user_id=user_id).order_by(FuelLog.date.desc()).all()
    logs_list = [log.to_dict() for log in logs]
    return jsonify({"fuel_logs": logs_list})


@fuel_log_bp.route("/update-fuel-log/<int:log_id>", methods=["PUT"])
def update_fuel_log_by_id(log_id):
    log = FuelLog.query.get(log_id)
    if not log:
        return jsonify({"error": "Fuel Log not found!"}), 404

    data = request.get_json()
    log.date = datetime.utcnow().date()
    log.litres = data.get("litres", log.litres)
    log.price = data.get("price", log.price)
    log.odometer = data.get("odometer", log.odometer)

    db.session.commit()
    return jsonify({"message": "Fuel log updated!", "fuel_log": log.to_dict()})

@fuel_log_bp.route("/delete-fuel-log/<int:log_id>", methods=["DELETE"])
def delete_fuel_log(log_id):
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "Unauthorized!"}), 401

    log = FuelLog.query.get(log_id)
    if not log or log.user_id != user_id:
        return jsonify({"error": "Fuel Log not found or unauthorized!"}), 404

    db.session.delete(log)
    db.session.commit()
    return jsonify({"message": "Fuel log deleted successfully!"}), 200
