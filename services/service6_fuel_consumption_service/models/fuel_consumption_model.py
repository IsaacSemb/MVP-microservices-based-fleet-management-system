from shared.database.db_utils import db

class FuelConsumption(db.Model):
    __tablename__ = 'fuel_consumption'

    fuel_id = db.Column(db.Integer, primary_key=True)
    vehicle_id = db.Column(db.Integer, nullable=False)  # Reference to the vehicle being refueled
    date = db.Column(db.Date, nullable=False)  # Date of the refueling
    fuel_type = db.Column(db.String(50), nullable=False)  # E.g., Diesel, Gasoline
    amount = db.Column(db.Float, nullable=False)  # Amount of fuel added (e.g., liters or gallons)
    cost = db.Column(db.Float, nullable=False)  # Cost of the refueling
    mileage = db.Column(db.Float, nullable=True)  # Mileage at the time of refueling, optional for consumption analysis

    def __init__(self, vehicle_id, date, fuel_type, amount, cost, mileage=None):
        self.vehicle_id = vehicle_id
        self.date = date
        self.fuel_type = fuel_type
        self.amount = amount
        self.cost = cost
        self.mileage = mileage

    def to_dict(self):
        return {
            "fuel_id": self.fuel_id,
            "vehicle_id": self.vehicle_id,
            "date": self.date.isoformat() if self.date else None,
            "fuel_type": self.fuel_type,
            "amount": self.amount,
            "cost": self.cost,
            "mileage": self.mileage
        }
