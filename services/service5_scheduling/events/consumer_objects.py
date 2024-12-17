from services.service5_scheduling.events.message_handlers import Message_handler 

# Instantiate the message handler for this service
handler = Message_handler()

# Define service-specific consumers

SERVICE_5_CONSUMERS = [
            {
                "queue_name": "service5_assignment_created_queue",
                "exchange": "assignment_created_fanout_exchange",
                "exchange_type": "fanout",
                "routing_key": "",
                "callback":handler.handle_event_created
            },
            {
                "queue_name": "service5_maintenance_created_queue",
                "exchange": "maintenance_created_fanout_exchange",
                "exchange_type": "fanout",
                "routing_key": "",
                "callback":handler.handle_event_created
            },
            {
                "queue_name": "service5_task_created_queue",
                "exchange": "task_created_fanout_exchange",
                "exchange_type": "fanout",
                "routing_key": "",
                "callback":handler.handle_event_created
            },
            {
                "queue_name": "service5_fuel_created_queue",
                "exchange": "fuel_record_fanout_exchange",
                "exchange_type": "fanout",
                "routing_key": "",
                "callback":handler.handle_event_created
            } 
                      
        ]