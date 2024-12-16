import json
import requests
import os

SERVICE_2_URL = os.getenv('SERVICE_2_URL')


class Message_handler:
    
    """this class hold all callback functions for handling different types of messages """
    
    
    def __init__(self):
        pass
    
    def default(self):
        msg = 'NOT A CONSUMER, NOTHING TO CONSUME'
        print(msg)
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
                print((f"Ignoring unsupported event type: {payload.get('event_type')}"))
                # logging.warning(f"Ignoring unsupported event type: {payload.get('event_type')}")
                # ch.basic_ack(delivery_tag=method.delivery_tag)
                return
            
            # testing purposes
            payload1= {
                'event_type': 'assignment_created', 
                'data': {'assignment_id': 25, 
                        'driver_id': 4, 
                        'vehicle_id': 5, 
                        'start_date_time': '2024-12-07T22:36:44', 
                        'end_date_time': None, 
                        'status': 'scheduled'
                        }
                }
            
            # extract data from the payload
            data = payload.get('data', {})
            
            # extract the vehicle id from the data
            vehicle_id = data.get('vehicle_id')
            
            print('\n\nthe payload\n',payload)
            print('\n\nthe payload data\n',payload.get('data', {}))
            print('\n\nthe vehicle_id from payload ----',data.get('vehicle_id'))
            
            
            if not vehicle_id:
                print("vehicle ID missing")
                # logging.error("vehicle ID is missing from the assignment message.")
                
                # Acknowledge message to avoid blocking the queue
                # ch.basic_ack(delivery_tag=method.delivery_tag)
                return
            
            
            
            else:
                print(f"vehicle ID is {vehicle_id}.\n")
                # logging.info(f"vehicle ID is {vehicle_id}.")
                
                # Acknowledge message to avoid blocking the queue
                # ch.basic_ack(delivery_tag=method.delivery_tag)
            
            # return
            
                
            # Prepare the URL and payload for the vehicle update
            url = f"{SERVICE_2_URL}/vehicles/{vehicle_id}"
            update_payload = {"status": "assigned"}

            # Make a PUT request to update the driver's status
            response = requests.put(url, json=update_payload, timeout=5)
            
            if response.status_code == 200:
                print(f"Driver with ID {vehicle_id} status changed successfully.")
            else:
                print(
                    f"Failed to update driver with ID {vehicle_id}.\n"
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
