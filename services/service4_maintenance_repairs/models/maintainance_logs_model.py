from common.database.db_utils import db
from sqlalchemy import Enum
from datetime import datetime, timezone
class MaintenanceLog(db.Model):
    __tablename__ = 'maintenance_logs'

    maintenance_id = db.Column(db.Integer, primary_key=True)
    vehicle_id = db.Column(db.Integer, nullable=False)
    maintenance_type = db.Column(
        Enum('routine', 'repair','unspecified', name='maintenance_type_status'), 
        nullable=False, 
        default='unspecified'
        )
    start_date_time = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    end_date_time = db.Column(db.DateTime, nullable=True)
    expected_completion_date_time = db.Column(db.DateTime, nullable=True)
    cost = db.Column(db.Float, nullable=True)
    description = db.Column(db.String(255), nullable=True)
    parts_used = db.Column(db.String(255), nullable=True)
    status = db.Column(
        Enum('scheduled', 'ongoing', 'cancelled','completed','overdue', name='maintenance_status'), 
        nullable=False, 
        default='scheduled')


    def __init__(self, vehicle_id, start_date_time,cost,end_date_time=None, description=None, parts_used=None, expected_completion_date_time=None, maintenance_type='unspecified', status='scheduled'):
        self.vehicle_id = vehicle_id
        self.maintenance_type = maintenance_type
        self.start_date_time = start_date_time or datetime.now(timezone.utc)
        self.end_date_time = end_date_time
        self.expected_completion_date_time = expected_completion_date_time
        self.cost = cost
        self.description = description
        self.parts_used = parts_used
        self.status = status

    def to_dict(self):
        return {
            "maintenance_id": self.maintenance_id,
            "vehicle_id": self.vehicle_id,
            "maintenance_type": self.maintenance_type,
            "start_date_time": self.start_date_time.isoformat() if self.start_date_time else None,
            "end_date_time": self.end_date_time.isoformat() if self.end_date_time else None,
            "expected_completion_date_time": self.expected_completion_date_time.isoformat() if self.expected_completion_date_time else None,
            "cost": self.cost,
            "description": self.description,
            "parts_used": self.parts_used,
            "status": self.status
        } 