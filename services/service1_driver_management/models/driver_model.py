from sqlalchemy import Enum
from common.database.db_utils import db



class Driver(db.Model):
    __tablename__ = 'drivers'

    driver_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    license_no = db.Column(db.String(50), unique=True, nullable=False)
    contact_info = db.Column(db.String(100), nullable=False)
    
    # Updated sex column with Enum for Male and Female
    sex = db.Column(
        Enum('Male', 'Female', name='gender_enum'),
        nullable=False
    )

    # Status Enum
    status = db.Column(
        Enum('available', 'assigned', 'active', 'unavailable', name='driver_status'),
        nullable=False,
        default='available'
    )
    
    """ 
    to fix values to a predetermined set
    we use the enum function
    """

    def __init__(self, first_name, last_name, license_no, contact_info, sex, status='available'):
        self.first_name = first_name
        self.last_name = last_name
        self.license_no = license_no
        self.contact_info = contact_info
        self.sex = sex
        self.status = status

    def __repr__(self):
        return f"<Driver {self.first_name} {self.last_name}>"
    
    def to_dict(self):
        return {
            "driver_id": self.driver_id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "license_no": self.license_no,
            "contact_info": self.contact_info,
            "sex": self.sex,
            "status": self.status
        }
