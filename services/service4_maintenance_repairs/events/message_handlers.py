import os
from common.logs.logger import logger



# callback funtion on message coming

class Message_handler:
    
    """this class hold all callback functions for handling different types of messages """
    
    def __init__(self):
        pass
    
    def default(self):
        msg = 'NOT A CONSUMER, NOTHING TO CONSUME'
        logger.debug(msg)
        return msg


      