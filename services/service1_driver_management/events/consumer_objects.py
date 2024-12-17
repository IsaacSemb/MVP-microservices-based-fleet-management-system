from services.service1_driver_management.events.message_handlers import Message_handler

# Instantiate the message handler for this service
handler = Message_handler()

# Define service-specific consumers

SERVICE_1_CONSUMERS = [
    {
        "queue_name": "driver_assignment_queue",
        "exchange": "assignment_created_fanout_exchange",
        "exchange_type": "fanout",
        "routing_key": "",
        "callback": handler.handle_assignment_created,
    },
    {
        "queue_name":"sample_driver_created",
        "exchange":"driver_created_fanout_exchange",
        "exchange_type":"fanout",
        "callback":handler.handle_driver_created
    },
    {
        "queue_name":"sample_vehicle_created",
        "exchange":"vehicle_created_fanout_exchange",
        "exchange_type":"fanout",
        "callback":handler.handle_vehicle_created
    }
]
