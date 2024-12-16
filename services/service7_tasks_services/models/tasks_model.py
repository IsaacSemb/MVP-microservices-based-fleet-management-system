from sqlalchemy import Enum, DateTime
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone
from shared.database.db_utils import db



class Task(db.Model):
    # table_name
    __tablename__ = 'tasks'

    # Primary Key
    task_id = db.Column(db.Integer, primary_key=True)

    # Columns
    task = db.Column(db.String(255), nullable=False)  # Task description
    assignment_id = db.Column(db.Integer, nullable=True)  # TASKS CAN BE UNASSIGNED IE FUTURE TASKS
    start_date_time = db.Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)  # Start Date-Time
    end_date_time = db.Column(DateTime, default=None)  # Actual End Date-Time
    expected_completion_date_time = db.Column(DateTime, default=None)  # Estimated End Date-Time
    description = db.Column(db.Text, nullable=True)  # Optional detailed description

    # Enums
    priority = db.Column(
        Enum('low', 'medium', 'high', 'critical', name='priority_levels'),
        nullable=False,
        default='low'
    )
    status = db.Column(
        Enum('scheduled', 'ongoing', 'cancelled', 'completed', name='task_status'),
        nullable=False,
        default='scheduled'
    )

    def __init__(
        self, 
        task, 
        assignment_id, 
        start_date_time=None, 
        expected_completion_date_time=None, 
        end_date_time=None, 
        description=None, 
        priority='low', 
        status='scheduled'
    ):
        self.task = task
        self.assignment_id = assignment_id
        self.start_date_time = start_date_time if start_date_time else datetime.now(timezone.utc)
        self.expected_completion_date_time = expected_completion_date_time
        self.end_date_time = end_date_time
        self.description = description
        self.priority = priority
        self.status = status

        
    def __repr__(self):
        return f"<Task {self.task}, Priority: {self.priority}, Status: {self.status}>"

    def to_dict(self):
        return {
            "task_id": self.task_id,
            "task": self.task,
            "assignment_id": self.assignment_id,
            "start_date_time": self.start_date_time.isoformat() if self.start_date_time else None,
            "expected_completion_date_time": self.expected_completion_date_time.isoformat() if self.expected_completion_date_time else None,
            "end_date_time": self.end_date_time.isoformat() if self.end_date_time else None,
            "description": self.description,
            "priority": self.priority,
            "status": self.status
        }



