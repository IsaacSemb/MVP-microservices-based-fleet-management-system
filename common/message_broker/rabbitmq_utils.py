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
        """Consume messages from a queue with manual acknowledgment."""
        try:
            connection, channel = self.create_connection()
            logger.info(f" [*] Consuming from queue '{queue_name}'")

            def wrapper_callback(ch, method, properties, body):
                try:
                    # Call the user-defined callback function
                    callback(ch, method, properties, body)
                    
                    # Manually acknowledge the message after successful processing
                    ch.basic_ack(delivery_tag=method.delivery_tag)
                    logger.info(f"Message acknowledged for delivery_tag: {method.delivery_tag}")
                except Exception as e:
                    # Log any error but do not acknowledge the message
                    logger.error(f"Error processing message: {e}, delivery_tag: {method.delivery_tag}")

            # Consume messages with manual acknowledgment
            channel.basic_consume(queue=queue_name, on_message_callback=wrapper_callback, auto_ack=False)

            # Start consuming
            channel.start_consuming()

        except KeyboardInterrupt:
            logger.info(f"Interrupted while consuming from {queue_name}")
        except Exception as e:
            logger.error(f"Error during consumption from {queue_name}: {e}")
        finally:
            if 'connection' in locals() and connection.is_open:
                connection.close()
                logger.info(f"Connection closed for queue '{queue_name}'")


    def publish_message(self, exchange, routing_key, message, exchange_type="direct"):
        """Publish a message to an exchange."""
        try:
            connection, channel = self.create_connection()

            # Declare the exchange before publishing to ensure it exists
            channel.exchange_declare(exchange=exchange, exchange_type=exchange_type, durable=True)

            # Publish the message
            channel.basic_publish(
                exchange=exchange,
                routing_key=routing_key,
                body=json.dumps(message),
                properties=pika.BasicProperties(delivery_mode=2)  # Persistent message
            )
            logger.info(f"Message published to exchange '{exchange}' with routing key '{routing_key}': {message}")

        except Exception as e:
            logger.error(f"Error publishing message: {e}")
        finally:
            if 'connection' in locals() and connection.is_open:
                connection.close()
                logger.info("Connection closed after publishing message.")


