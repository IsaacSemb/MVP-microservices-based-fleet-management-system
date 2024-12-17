from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Enum
from common.database.db_utils import db
from datetime import datetime, timezone

class Schedule(db.Model):
    __tablename__ = 'schedules'

    schedule_id = db.Column(db.Integer, primary_key=True)
    schedule_type = db.Column(Enum('maintenance', 'task', 'assignment', name='schedule_type_status'), nullable=False)
    schedule_type_id = db.Column(db.Integer, nullable=True)
    start_date_time = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    end_date_time = db.Column(db.DateTime, nullable=True)
    expected_completion = db.Column(db.DateTime, nullable=True)
    status = db.Column(Enum('scheduled', 'ongoing', 'cancelled', 'completed', 'overdue', 'active', name='schedule_status'), nullable=False, default='scheduled')
    description = db.Column(db.String(255), nullable=True)

    def __init__(self, schedule_type, start_date_time, schedule_type_id=None, end_date_time=None, expected_completion=None, status='scheduled', description=None):
        self.schedule_type = schedule_type
        self.start_date_time = start_date_time or datetime.now(timezone.utc)
        self.schedule_type_id = schedule_type_id
        self.end_date_time = end_date_time 
        self.expected_completion = expected_completion
        self.status = status
        self.description = description

    def to_dict(self):
        return {
            "schedule_id": self.schedule_id,
            "schedule_type": self.schedule_type,
            "schedule_type_id": self.schedule_type_id,
            "start_date_time": self.start_date_time.isoformat() if self.start_date_time else None,
            "end_date_time": self.end_date_time.isoformat() if self.end_date_time else None,
            "expected_completion": self.expected_completion.isoformat() if self.expected_completion else None,
            "status": self.status,
            "description": self.description 
        }
