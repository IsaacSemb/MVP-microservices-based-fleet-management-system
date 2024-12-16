import json
import requests
import os

SERVICE_3_URL = os.getenv('SERVICE_3_URL')


class Message_handler:
    
    """this class hold all callback functions for handling different types of messages """
    
    def __init__(self):
        pass
    
    def default(self):
        msg = 'NOT A CONSUMER, NOTHING TO CONSUME'
        print(msg)
        return msg
    

