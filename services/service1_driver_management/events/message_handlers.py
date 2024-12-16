import json
import requests
import os
from shared.logs.logger import logger

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
    
    def handle_assignment_created(self, ch, method, properties, body):
        """
        Callback function for consuming assignment-created messages.
        """
        
        try:
            # Parse the message body
            payload = json.loads(body)
            
            # Filter by event type
            if payload.get('event_type') != 'assignment_created':
                logger.debug((f"Ignoring unsupported event type: {payload.get('event_type')}"))
                # logging.warning(f"Ignoring unsupported event type: {payload.get('event_type')}")
                # ch.basic_ack(delivery_tag=method.delivery_tag)
                return
            
            
            # extract data from the payload
            data = payload.get('data', {})
            
            # extract the driver id from the data
            driver_id = data.get('driver_id')
            
            print('\n\nthe payload\n',payload)
            print('\n\nthe payload data\n',payload.get('data', {}))
            print('\n\nthe driver_id from payload ----',data.get('driver_id'))
            
            
            if not driver_id:
                print("Driver ID missing")
                # logging.error("Driver ID is missing from the assignment message.")
                
                # Acknowledge message to avoid blocking the queue
                # ch.basic_ack(delivery_tag=method.delivery_tag)
                return
            
            else:
                print(f"Driver ID is {driver_id}.\n")
                # logging.info(f"Driver ID is {driver_id}.")
                
                # Acknowledge message to avoid blocking the queue
                # ch.basic_ack(delivery_tag=method.delivery_tag)
                
                
            # Prepare the URL and payload for the driver update
            url = f"{SERVICE_1_URL}/drivers/{driver_id}"
            update_payload = {"status": "assigned"}

            # Make a PUT request to update the driver's status
            response = requests.put(url, json=update_payload, timeout=5)
            
            if response.status_code == 200:
                print(f"Driver with ID {driver_id} status changed successfully.")
            else:
                print(
                    f"Failed to update driver with ID {driver_id}.\n"
                    f"Status code: {response.status_code}, Response: {response.text}\n"
                )

            # Acknowledge the message
            # ch.basic_ack(delivery_tag=method.delivery_tag)

        # incase of requests error
        except requests.RequestException as e:
            print(f"Network error while updating driver status: {e}")

        # incase the json payload has issues
        except json.JSONDecodeError as e:
            print(f"Failed to parse message payload: {e}")
            # ch.basic_ack(delivery_tag=method.delivery_tag)

        # any other error
        except Exception as e:
            print(f"Unexpected error: {e}")

