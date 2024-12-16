
import os
from shared.database.db_utils import db
from shared.message_broker.rabbitmq_utils import RabbitMQ

broker = RabbitMQ()

SERVICE_7_URL = os.getenv('SERVICE_7_URL')


class Message_handler:
    
    """this class hold all callback functions for handling different types of messages """
        
    def __init__(self):
        pass
    
    def default(self):
        msg = 'NOT A CONSUMER, NOTHING TO CONSUME'
        print(msg)
        return msg
    
    
    def tasks_details_requested(self, ch, method, properties, body):
        """
        this call back send task details based on a task ID back to the broker
        for whoever needs them
        """
        pass
    

