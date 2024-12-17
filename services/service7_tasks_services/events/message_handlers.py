
import os
from common.database.db_utils import db
from common.message_broker.rabbitmq_utils import RabbitMQ

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
    
    

