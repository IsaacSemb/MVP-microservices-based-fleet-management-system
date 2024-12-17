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

      