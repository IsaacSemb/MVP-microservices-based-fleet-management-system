import pika
import json
import os
import sys
import threading
from common.logs.logger import logger


class RabbitMQ:
    """This class holds all utility functions and variables for RabbitMQ message broker"""

    def __init__(self, host=None, port=None):
        self.host = host or os.getenv("RABBITMQ_HOST", "localhost")
        self.port = port or int(os.getenv("RABBITMQ_PORT", 5672))

    def create_connection(self):
        """Create a new connection and channel."""
        connection_params = pika.ConnectionParameters(host=self.host, port=self.port)
        connection = pika.BlockingConnection(connection_params)
        channel = connection.channel()
        return connection, channel

    def declare_exchange_and_queue(self, channel, exchange, exchange_type, queue, routing_key=""):
        """Declare an exchange and a queue, and bind them."""
        channel.exchange_declare(exchange=exchange, exchange_type=exchange_type, durable=True)
        channel.queue_declare(queue=queue, durable=True)
        channel.queue_bind(queue=queue, exchange=exchange, routing_key=routing_key)

    def consume_messages(self, queue_name, callback):
        """Consume messages from a queue."""
        try:
            connection, channel = self.create_connection()
            channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
            logger.info(f" [*] Consuming from queue '{queue_name}'")
            channel.start_consuming()
        except KeyboardInterrupt:
            logger.info(f"Interrupted while consuming from {queue_name}")
        except Exception as e:
            logger.error(f"Error during consumption from {queue_name}: {e}")
        finally:
            if 'connection' in locals() and connection.is_open:
                connection.close()
                logger.info(f"Connection closed for queue '{queue_name}'")


# Consumer Configuration Object
class ConsumerConfig:
    """A class to hold consumer details such as queues, callbacks, and exchanges"""

    def __init__(self, queue_name, exchange, exchange_type, callback, routing_key=""):
        self.queue_name = queue_name
        self.exchange = exchange
        self.exchange_type = exchange_type
        self.callback = callback
        self.routing_key = routing_key


# Define Callbacks
def process_the_task1(ch, method, properties, body):
    msg = body.decode('utf-8')
    logger.info(f"Received message: {msg}, Callback: {process_the_task1.__name__}")


def process_the_task2(ch, method, properties, body):
    msg = body.decode('utf-8')
    logger.info(f"Received message: {msg}, Callback: {process_the_task2.__name__}")


if __name__ == '__main__':
    try:
        # Initialize RabbitMQ object
        rabbitmq = RabbitMQ()

        # List of consumer configurations
        consumers = [
            ConsumerConfig(
                queue_name="sample_driver_created",
                exchange="driver_created_fanout_exchange",
                exchange_type="fanout",
                callback=process_the_task1
            ),
            ConsumerConfig(
                queue_name="sample_vehicle_created",
                exchange="vehicle_created_fanout_exchange",
                exchange_type="fanout",
                callback=process_the_task2
            )
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
