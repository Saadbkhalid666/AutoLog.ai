from flask import Blueprint, request, jsonify
from utils.extensions import db
from models.fuel_log import FuelLog
from datetime import datetime

fuel_log_bp = Blueprint("fuel_log", __name__)

@fuel_log_bp.route("/log/manual", methods=["POST"])
def create_fuel_log():
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
        mileage=data.get("mileage")
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
            "mileage": fuel_log.mileage
        }
    }), 201
