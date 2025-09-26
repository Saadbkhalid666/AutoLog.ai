import os
import pytesseract
from flask import Blueprint, request, jsonify
from utils.extensions import db
from models.fuel_log import FuelLog
from datetime import datetime
from PIL import Image

fuel_log_bp = Blueprint("vehicle", __name__)

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


@fuel_log_bp.route("/fuel-log/manual", methods=["POST"])
def post_manual_fuel_log():
    data = request.get_json()

    # agar date na mile to default = today
    date_value = data.get("date")
    if date_value:
        date_value = datetime.fromisoformat(date_value).date()
    else:
        date_value = datetime.utcnow().date()

    fuel_log = FuelLog(
        user_id=data.get("user_id"),
        date=date_value,
        litres=data.get("litres"),
        price=data.get("price"),
        odometer=data.get("odometer")
    )

    db.session.add(fuel_log)
    db.session.commit()

    return jsonify({
        "message": "Fuel log created successfully",
        "fuel_log": {
            "id": fuel_log.id,
            "user_id": fuel_log.user_id,
            "date": fuel_log.date.isoformat(),
            "litres": fuel_log.litres,
            "price": fuel_log.price,
            "odometer": fuel_log.odometer
        }
    }), 201

@fuel_log_bp.route("/fuel-logs/ocr", methods=["POST"])
def post_ocr_fuel_log():
    if "file" not in request.files:
        return jsonify({"error":"No file Uploaded!"}),400
    
    file = request.files["file"]
    filepath = os.path.join("uploads",file.filename)
    file.save(filepath)

    img = Image.open(filepath)
    text = pytesseract.image_to_string(img)

    litres = "50"
    price = "4000"
    odometer = "12345"
    date = datetime.utcnow().date()

    fuel_log = FuelLog(
        user_id=1,  # replace with actual user id
        date=date,
        litres=litres,
        price=price,
        odometer=odometer
    )

    db.session.add(fuel_log)
    db.session.commit()

    return jsonify({
        "extracted_text":text,
        "fuel_log":{
            "date":date,
            "litres":litres,
            "price":price,
            "odometer":odometer
        }
    })

 