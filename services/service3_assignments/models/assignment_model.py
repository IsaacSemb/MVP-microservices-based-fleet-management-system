from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Enum
from datetime import datetime, timezone
from common.database.db_utils import db

class Assignment(db.Model):
    __tablename__ = 'assignments'

    assignment_id = db.Column(db.Integer, primary_key=True)
    driver_id = db.Column(db.Integer, nullable=False)
    vehicle_id = db.Column(db.Integer, nullable=False)
    start_date_time = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    end_date_time = db.Column(db.DateTime, nullable=True)  # Could be None if ongoing assignment
    status = db.Column(Enum('completed', 'active', 'cancelled', 'scheduled', name='assignment_status_enum'), nullable=False, default='scheduled')

    def __init__(self, driver_id, vehicle_id, start_date_time=None, end_date_time=None, status='scheduled'):
        self.driver_id = driver_id
        self.vehicle_id = vehicle_id
        self.start_date_time = start_date_time or datetime.now(timezone.utc)
        self.end_date_time = end_date_time
        self.status = status
    
    def to_dict(self):
        return {
            "assignment_id": self.assignment_id,
            "driver_id": self.driver_id,
            "vehicle_id": self.vehicle_id,
            "start_date_time": self.start_date_time.isoformat() if self.start_date_time else None,
            "end_date_time": self.end_date_time.isoformat() if self.end_date_time else None,
            "status": self.status
        }
