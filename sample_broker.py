import pika
import json
import os
import sys
from common.logs.logger import logger

class RabbitMQ:
    """This class holds all utility functions and variables for RabbitMQ message broker"""

    def __init__(self, host=None, port=None):
        self.host = host or os.getenv("RABBITMQ_HOST", "localhost")
        self.port = port or int(os.getenv("RABBITMQ_PORT", 5672))
        self.connection = None
        self.channel = None

    def connect(self):
        """Establish connection to RabbitMQ."""
        try:
            connection_params = pika.ConnectionParameters(host=self.host, port=self.port)
            self.connection = pika.BlockingConnection(connection_params)
            self.channel = self.connection.channel()
        except pika.exceptions.AMQPConnectionError as e:
            logger.warning(f"Failed to connect to RabbitMQ: {e}")
            raise

    def close_connection(self):
        """Close the RabbitMQ connection."""
        if self.connection:
            self.connection.close()

    def declare_exchange(self, exchange, exchange_type="direct"):
        """Declare an exchange."""
        self.channel.exchange_declare(exchange=exchange, exchange_type=exchange_type, durable=True)

    def declare_and_bind_queue(self, queue, exchange, routing_key=""):
        """Declare a queue and bind it to an exchange."""
        self.channel.queue_declare(queue=queue, durable=True)
        self.channel.queue_bind(queue=queue, exchange=exchange, routing_key=routing_key)

    def consume_messages(self, queue_name, callback):
        """Consume messages from a queue."""
        try:
            self.connect()
            self.channel.basic_consume(
                queue=queue_name,
                on_message_callback=callback,
                auto_ack=True
            )
            logger.info(f" [*] Consuming from queue '{queue_name}'")
            self.channel.start_consuming()
        except KeyboardInterrupt:
            logger.info("Consumer interrupted by user.")
        except Exception as e:
            logger.error(f"Error during consumption: {e}")
        finally:
            self.close_connection()


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

        for consumer in consumers:
            # Connect, declare exchange, declare/bind queue
            rabbitmq.connect()
            rabbitmq.declare_exchange(consumer.exchange, consumer.exchange_type)
            rabbitmq.declare_and_bind_queue(
                queue=consumer.queue_name,
                exchange=consumer.exchange,
                routing_key=consumer.routing_key
            )
            rabbitmq.close_connection()

        # Start consuming for each queue
        print(" [*] Waiting for messages. To exit press CTRL+C")
        for consumer in consumers:
            rabbitmq.consume_messages(queue_name=consumer.queue_name, callback=consumer.callback)

    except KeyboardInterrupt:
        print("Interrupted")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
