from utils.extensions import db
from datetime import datetime

class FuelLog(db.Model):
    __tablename__ = "fuel_log"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, primary_key=False)
    date = db.Column(db.Date, nullable=False, default=datetime.utcnow) 
    litres = db.Column(db.Float, nullable=False)
    price = db.Column(db.Float, nullable=False)
    odometer = db.Column(db.Integer, nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<FuelLog user_id={self.user_id} date={self.date}>"
    
    def to_dict(self):
       return {
            "id": self.id,
            "user_id": self.user_id,
            "date": self.date.isoformat(),  
            "litres": self.litres,
            "price": self.price,
            "odometer": self.odometer,
            "created_at": self.created_at.isoformat()
        }
