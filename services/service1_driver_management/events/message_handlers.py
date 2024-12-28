import json
import os
from common.logs.logger import logger
from services.service1_driver_management.models.driver_model import Driver
from services.service1_driver_management.app import app
from common.database.db_utils import db

SERVICE_1_URL = os.getenv('SERVICE_1_URL')

# callback funtion on message coming

class Message_handler:
    
    """this class hold all callback functions for handling different types of messages """
    
    def __init__(self):
        pass
    
    def default(self):
        msg = 'NOT A CONSUMER, NOTHING TO CONSUME'
        logger.debug(msg)
        return msg
    
    def handle_driver_created(self, ch, method, properties, body):
        logger.info(body)
            
    def handle_vehicle_created(self, ch, method, properties, body):
        logger.info(body)
            
    def handle_assignment_created(self, ch, method, properties, body):
        """
        Callback function for consuming assignment-created messages.
        """
        try:
            # Parse the message body
            payload = json.loads(body)
            
            logger.info(payload)
            
            # Filter by event type
            if payload.get('event_type') != 'new_assignment_created':
                logger.warning(f"Ignoring unsupported event type: {payload.get('event_type')}")
                return
            
            with app.app_context():
            
                # Extract data from the payload
                data = payload.get('data', {})
                
                # Extract the driver ID from the data
                driver_id = data.get('driver_id')
                logger.info(f"Received assignment_created event: {payload}")
                
                if not driver_id:
                    logger.error("Driver ID missing in the assignment message.")
                    return
                
                # Query the Driver model for the given driver_id
                driver = Driver.query.filter_by(driver_id=driver_id).first()
                
                if not driver:
                    logger.error(f"Driver with ID {driver_id} not found in the database.")
                    return
                
                # Update driver's status to 'assigned'
                try:
                    driver.status = "assigned"
                    db.session.commit()
                    logger.info(f"Driver ID {driver_id} status successfully updated to 'assigned'.")
                except Exception as db_error:
                    db.session.rollback()
                    logger.error(f"Database error while updating driver status: {str(db_error)}")
                    return
                
                logger.info(f"Driver with ID {driver_id} status updated successfully.")

        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse message payload: {str(e)}")

        except Exception as e:
            logger.error(f"Unexpected error while handling the assignment-created message: {str(e)}")
