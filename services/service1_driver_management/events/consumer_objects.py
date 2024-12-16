from services.service1_driver_management.tasks.message_handlers import Message_handler

# Instantiate the message handler for this service
handler = Message_handler()

# Define service-specific consumers

SERVICE_1_CONSUMERS = [
    {
        "queue_name": "driver_assignment_queue",
        "exchange": "assignment_created_fanout_exchange",
        "exchange_type": "fanout",
        "routing_key": "",
        "handler": handler.handle_assignment_created,
    },
    # {
    #     "queue_name": "driver_status_queue",
    #     "exchange": "driver_status_exchange",
    #     "exchange_type": "direct",
    #     "routing_key": "driver.status",
    #     "handler": "handle_driver_status_update",
    # },
]
