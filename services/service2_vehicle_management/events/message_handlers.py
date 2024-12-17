import json
import os
from common.logs.logger import logger
from services.service2_vehicle_management.models.vehicle_model import Vehicle
from services.service2_vehicle_management.app import app
from common.database.db_utils import db


SERVICE_2_URL = os.getenv('SERVICE_2_URL')


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
            
            # Filter by event type
            if payload.get('event_type') != 'assignment_created':
                logger.warning(f"Ignoring unsupported event type: {payload.get('event_type')}")
                return
            
            with app.app_context():
            
                # Extract data from the payload
                data = payload.get('data', {})
                
                # Extract the vehicle ID from the data
                vehicle_id = data.get('vehicle_id')
                logger.info(f"Received assignment_created event: {payload}")
                
                if not vehicle_id:
                    logger.error("vehicle ID missing in the assignment message.")
                    return
                
                # Query the vehicle model for the given vehicle_id
                vehicle = Vehicle.query.filter_by(vehicle_id=vehicle_id).first()
                
                if not vehicle:
                    logger.error(f"vehicle with ID {vehicle_id} not found in the database.")
                    return
                
                # Update vehicle's status to 'assigned'
                try:
                    vehicle.status = "assigned"
                    db.session.commit()
                    logger.info(f"vehicle ID {vehicle_id} status successfully updated to 'assigned'.")
                except Exception as db_error:
                    db.session.rollback()
                    logger.error(f"Database error while updating vehicle status: {str(db_error)}")
                    return
                
                logger.info(f"vehicle with ID {vehicle_id} status updated successfully.")

        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse message payload: {str(e)}")

        except Exception as e:
            logger.error(f"Unexpected error while handling the assignment-created message: {str(e)}")
