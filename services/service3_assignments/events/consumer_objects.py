from services.service3_assignments.events.message_handlers import Message_handler

# Instantiate the message handler for this service
handler = Message_handler()


SERVICE_3_CONSUMERS = [
        {
            "queue_name":"service3_driver_created",
            "exchange":"driver_created_fanout_exchange",
            "exchange_type":"fanout",
            "callback":handler.handle_driver_created
        },
        {
            "queue_name":"service3_vehicle_created",
            "exchange":"vehicle_created_fanout_exchange",
            "exchange_type":"fanout",
            "callback":handler.handle_vehicle_created
        }
    ]
