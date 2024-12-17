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
            "callback":handler.handle_assignment_created            
        },
        {
            "queue_name":"service2_driver_created",
            "exchange":"driver_created_fanout_exchange",
            "exchange_type":"fanout",
            "callback":handler.handle_driver_created
        },
        {
            "queue_name":"service2_vehicle_created",
            "exchange":"vehicle_created_fanout_exchange",
            "exchange_type":"fanout",
            "callback":handler.handle_vehicle_created
        }
    ]
    

