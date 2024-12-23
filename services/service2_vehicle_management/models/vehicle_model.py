from common.database.db_utils import db
from sqlalchemy import Enum


class Vehicle(db.Model):
    __tablename__ = 'vehicles'
    
    vehicle_id = db.Column(db.Integer, primary_key=True)
    make = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(50), nullable=False)
    reg_no = db.Column(db.String(20), unique=True, nullable=False)
    
    fuel_type = db.Column(
        Enum('petrol', 'diesel', 'electric', 'hybrid', 'not_specified', name='fuel_type_enum'), 
        nullable=False, 
        default='not_specified'
    )
    
    vehicle_type = db.Column(
        Enum('car', 'truck', 'van', 'bus', 'not_specified', name='vehicle_type_enum'), 
        nullable=False, 
        default='not_specified'
    )
    
    status = db.Column(
        Enum('available', 'assigned', 'service', 'on_leave', name='vehicle_status'), 
        nullable=False, 
        default='available'
    )
    
    def __init__(self, make, model, reg_no, fuel_type, vehicle_type, status='available'):
        self.make = make
        self.model = model
        self.reg_no = reg_no
        self.fuel_type = fuel_type
        self.vehicle_type = vehicle_type
        self.status = status

    def __repr__(self):
        return f"<Vehicle {self.make} {self.model}>"
    
    def to_dict(self):
        return {
            "vehicle_id": self.vehicle_id,
            "make": self.make,
            "model": self.model,
            "reg_no": self.reg_no,
            "fuel_type": self.fuel_type,
            "vehicle_type": self.vehicle_type,
            "status": self.status
        }
