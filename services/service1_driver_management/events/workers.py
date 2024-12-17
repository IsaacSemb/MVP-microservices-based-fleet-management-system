import os
import sys
import threading

# Add the project root directory to sys.path
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
sys.path.append(root_path)

# Now import the common module
from common.message_broker.consumer_manager import start_consumer_processes
from common.message_broker.rabbitmq_utils import RabbitMQ
from common.logs.logger import logger
from common.message_broker.consumer_config import ConsumerConfig
from consumer_objects import SERVICE_1_CONSUMERS



if __name__ == '__main__':
    try:
        # Initialize RabbitMQ object
        rabbitmq = RabbitMQ()

        # List of consumer configurations
        # Convert each dictionary into a ConsumerConfig object
        consumers = [
        ConsumerConfig(
            queue_name=consumer["queue_name"],
            exchange=consumer["exchange"],
            exchange_type=consumer["exchange_type"],
            callback=consumer["callback"],
            routing_key=consumer.get("routing_key", "")
        )
        for consumer in SERVICE_1_CONSUMERS
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
        
        print(" [*] Waiting for messages. To exit press CTRL+C")
        

    except KeyboardInterrupt:
        print("Interrupted")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
