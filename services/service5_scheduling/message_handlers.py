
import json
import requests
import os

SERVICE_5_URL = os.getenv('SERVICE_5_URL')


class Message_handler:
    """this class hold an assortment of callback functions for handling different types of messages"""
    def __init__(self):
        self.responses = []

    def default(self):
        msg = 'NOT A CONSUMER, NOTHING TO CONSUME'
        print(msg)
        return msg
    
    
    
    def handle_event_created(self, ch, method, properties, body):
        data = json.loads(body)
        event_type = data["event_type"]
        schedule_data = data["data"]



        if event_type == "assignment_created":
            # Add assignment to schedule
            try:
                # Parse the message body
                payload = json.loads(body)
                
                # Filter by event type
                if payload.get('event_type') != 'assignment_created':
                    print((f"Ignoring unsupported event type: {payload.get('event_type')}"))
                    # logging.warning(f"Ignoring unsupported event type: {payload.get('event_type')}")
                    # ch.basic_ack(delivery_tag=method.delivery_tag)
                    return
                
                
                # extract data from the payload
                data = payload.get('data', {})
                
                # extract the assignment id from the data
                assignment_id = data.get('assignment_id')
                
                print('\n\nthe payload\n',payload)
                print('\n\nthe payload data\n',payload.get('data', {}))
                print('\n\nthe assignment_id from payload ----',data.get('assignment_id'))
                
                
                if not assignment_id:
                    print("assignment ID missing")
                    # logging.error("assignment ID is missing from the assignment message.")
                    
                    # Acknowledge message to avoid blocking the queue
                    # ch.basic_ack(delivery_tag=method.delivery_tag)
                    return
                
                
                
                else:
                    print(f"assignment ID is {assignment_id}.\n")
                    # logging.info(f"assignment ID is {vehicle_id}.")
                    
                    # Acknowledge message to avoid blocking the queue
                    # ch.basic_ack(delivery_tag=method.delivery_tag)
                
                # return
                
                    
                # Prepare the URL and payload for the vehicle update
                url = f"{SERVICE_5_URL}/schedules"
                
                schedule_payload = data
                
                print(schedule_payload)
                
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
                
                new_maintenance = {
                    "schedule_type_id":data.get('assignment_id'),
                    "schedule_type":"assignment",
                    "start_date_time":data.get('start_date_time'), 
                    "end_date_time":data.get('end_date_time'),
                    "expected_completion":data.get('expected_completion_date_time'),
                    "status":data.get('status', 'scheduled'),
                    "description":data.get('description')
                    }
                
                print(new_maintenance)
                
                
                # return

                # Make a POSTT request to update the driver's status
                response = requests.post(url, json=new_maintenance, timeout=5)
                
                if response.status_code == 200 or response.status_code == 201 :
                    print(f"Assignment ID {assignment_id} has been added successfully.")
                else:
                    print(
                        f"Failed to add assignment with ID {assignment_id}.\n"
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
                
                
        
        elif event_type == "maintenance_created":
            # Add maintenance to schedule
            try:
                # Parse the message body
                payload = json.loads(body)
                
                # Filter by event type
                if payload.get('event_type') != 'maintenance_created':
                    print((f"Ignoring unsupported event type: {payload.get('event_type')}"))
                    # logging.warning(f"Ignoring unsupported event type: {payload.get('event_type')}")
                    # ch.basic_ack(delivery_tag=method.delivery_tag)
                    return
                
                
                # extract data from the payload
                data = payload.get('data', {})
                
                # extract the maintenance id from the data
                maintenance_id = data.get('maintenance_id')
                
                print('\n\nthe payload\n',payload)
                print('\n\nthe payload data\n',payload.get('data', {}))
                print('\n\nthe maintenance_id from payload ----',data.get('maintenance_id'))
                
                
                if not maintenance_id:
                    print("maintenance ID missing")
                    # logging.error("maintenance ID is missing from the maintenance message.")
                    
                    # Acknowledge message to avoid blocking the queue
                    # ch.basic_ack(delivery_tag=method.delivery_tag)
                    return
                
                
                
                else:
                    print(f"maintenance ID is {maintenance_id}.\n")
                    # logging.info(f"maintenance ID is {vehicle_id}.")
                    
                    # Acknowledge message to avoid blocking the queue
                    # ch.basic_ack(delivery_tag=method.delivery_tag)
                
                # return
                
                    
                # Prepare the URL and payload for the vehicle update
                url = f"{SERVICE_5_URL}/schedules"
                
                schedule_payload = data
                
                print(schedule_payload)
                
                payload1=  {
                    'event_type': 'maintenance_created',
                    'data': {
                        'maintenance_id': 1,
                        'vehicle_id': 4,
                        'maintenance_type': 'repair',
                        'start_date_time': '2023-11-26T00:00:00',
                        'end_date_time': None,
                        'expected_completion_date_time': '2023-12-01T00:00:00',
                        'cost': None,
                        'description': 'Engine overhaul due to overheating issue.',
                        'parts_used': 'Pistons,Gaskets, Coolant, Spark plugs',
                        'status': 'overdue'
                        }
                    }
                
                new_maintenance = {
                    "schedule_type_id":data.get('maintenance_id'),
                    "schedule_type":"maintenance",
                    "start_date_time":data.get('start_date_time'), 
                    "end_date_time":data.get('end_date_time'),
                    "expected_completion":data.get('expected_completion_date_time'),
                    "status":data.get('status', 'scheduled'),
                    "description":data.get('description')
                    }
                
                print(new_maintenance)
                
                
                # return

                # Make a POST request to update the driver's status
                response = requests.post(url, json=new_maintenance, timeout=5)
                
                if response.status_code == 200 or response.status_code == 201 :
                    print(f"maintenance ID {maintenance_id} has been added successfully.")
                else:
                    print(
                        f"Failed to add maintenance with ID {maintenance_id}.\n"
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
        
        
            
        elif event_type == "task_created":
            # Add maintenance to schedule
            try:
                # Parse the message body
                payload = json.loads(body)
                
                # Filter by event type
                if payload.get('event_type') != 'task_created':
                    print((f"Ignoring unsupported event type: {payload.get('event_type')}"))
                    # logging.warning(f"Ignoring unsupported event type: {payload.get('event_type')}")
                    # ch.basic_ack(delivery_tag=method.delivery_tag)
                    return
                
                
                # extract data from the payload
                data = payload.get('data', {})
                
                # extract the task id from the data
                task_id = data.get('task_id')
                
                print('\n\nthe payload\n',payload)
                print('the payload data\n',payload.get('data', {}))
                print('nthe task_id from payload ----',data.get('task_id'))
                print('')
                
                
                if not task_id:
                    print("task ID missing")
                    # logging.error("task ID is missing from the task message.")
                    
                    # Acknowledge message to avoid blocking the queue
                    # ch.basic_ack(delivery_tag=method.delivery_tag)
                    return
                                
                else:
                    print(f"task ID is {task_id}.\n")
                    # logging.info(f"maintenance ID is {vehicle_id}.")
                    
                    # Acknowledge message to avoid blocking the queue
                    # ch.basic_ack(delivery_tag=method.delivery_tag)
                    
                    
                # Prepare the URL and payload for the vehicle update
                url = f"{SERVICE_5_URL}/schedules"
                
                schedule_payload = data
                
                print(schedule_payload)

                
                new_task = {
                    "schedule_type_id":data.get('task_id'),
                    "schedule_type":"task",
                    "start_date_time":data.get('start_date_time'), 
                    "end_date_time":data.get('end_date_time'),
                    "expected_completion":data.get('expected_completion_date_time'),
                    "status":data.get('status', 'scheduled'),
                    "description":data.get('description')
                    }
                
                print(new_task)
                
                
                # return

                # Make a POST request to update the driver's status
                response = requests.post(url, json=new_task, timeout=5)
                
                if response.status_code == 200 or response.status_code == 201 :
                    print(f"task ID {task_id} has been added successfully.")
                else:
                    print(
                        f"Failed to add task with ID {task_id}.\n"
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
    
    
    def    receive_schedule_type_id_details(self, ch, method, properties, body):
        """
        Callback for handling responses from task, maintenance, or assignment services.
        """
        try:
            # Deserialize the response message
            response = json.loads(body)
            print(f"Received response: {response}")
            self.responses.append(response)
            print(self.responses)


        except Exception as e:
            print(f"Error in received_schedule_type_id_details: {e}")

   