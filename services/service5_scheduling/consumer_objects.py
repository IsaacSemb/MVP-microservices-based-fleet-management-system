from services.service5_scheduling.message_handlers import Message_handler 

# Instantiate the message handler for this service
handler = Message_handler()

# Define service-specific consumers

SERVICE_5_CONSUMERS = [
            {
                "queue_name": "assignment_created_queue",
                "exchange": "assignment_created_fanout_exchange",
                "exchange_type": "fanout",
                "routing_key": "",
                "handler":handler.handle_event_created
            },
            {
                "queue_name": "maintenance_created_queue",
                "exchange": "maintenance_created_direct_exchange",
                "exchange_type": "direct",
                "routing_key": "maintenance.created",
                "handler":handler.handle_event_created
            },
            {
                "queue_name": "task_created_queue",
                "exchange": "task_created_direct_exchange",
                "exchange_type": "direct",
                "routing_key": "task.created",
                "handler":handler.handle_event_created
            },
            # {
            #     # Scheduler Consumer for Task, Maintenance, and Assignment Responses
            #     "queue_name": "schedule_type_id_details_response_queue",
            #     "exchange": "schedule_exchange",
            #     "exchange_type": "direct",  
            #     "routing_key": "schedule_type_id_details_response_queue",  
            #     "handler": handler.receive_schedule_type_id_details  
            # }
            
        ]