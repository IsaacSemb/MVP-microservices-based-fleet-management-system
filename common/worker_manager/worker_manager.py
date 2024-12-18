import os
import sys
import threading
from common.message_broker.rabbitmq_utils import RabbitMQ
from common.message_broker.consumer_config import ConsumerConfig
from common.logs.logger import logger
import time

def start_service_workers(service_consumers):
    """
    Starts the workers for the given list of consumers.

    Args:
        service_consumers (list): List of consumer configurations (dictionaries).
    """
    try:
        
        while True:
            # Check if the service has workers
            while len(service_consumers) == 0:
                logger.info("NO CONSUMERS FOUND! Retrying in 60 seconds...")
                time.sleep(60)  # Wait before checking again
                continue
            
            
            # Initialize RabbitMQ object
            rabbitmq = RabbitMQ()

            # Convert consumer configurations into ConsumerConfig objects
            consumers = [
                ConsumerConfig(
                    queue_name=consumer["queue_name"],
                    exchange=consumer["exchange"],
                    exchange_type=consumer["exchange_type"],
                    callback=consumer["callback"],
                    routing_key=consumer.get("routing_key", "")
                )
                for consumer in service_consumers
            ]

            # Declare exchanges and queues
            for consumer in consumers:
                connection, channel = rabbitmq.create_connection()
                rabbitmq.declare_exchange_and_queue(
                    channel=channel,
                    exchange=consumer.exchange,
                    exchange_type=consumer.exchange_type,
                    queue=consumer.queue_name,
                    routing_key=consumer.routing_key
                )
                connection.close()

            # Start each consumer in its own thread
            threads = []
            for consumer in consumers:
                thread = threading.Thread(
                    target=rabbitmq.consume_messages, 
                    args=(consumer.queue_name, consumer.callback),
                    daemon=True
                )
                thread.start()
                threads.append(thread)
                logger.info(f"Started consumer for queue: {consumer.queue_name}")

            # Keep the main thread alive
            for thread in threads:
                thread.join()

    except KeyboardInterrupt:
        logger.info("Worker process interrupted.")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Error starting workers: {e}")
        sys.exit(1)
