from services.service2_vehicle_management.events.message_handlers import Message_handler

# Instantiate the message handler for this service
handler = Message_handler()

# Define service-specific consumers

SERVICE_2_CONSUMERS = [
        {
            "queue_name": "vehicle_assignment_queue",
            "exchange": "assignment_created_fanout_exchange",
            "exchange_type": "fanout",
            "routing_key": "",
            "handler":handler.handle_assignment_created
            
        }
    ]
    

