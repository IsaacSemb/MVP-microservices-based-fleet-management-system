import pika
import json
import os
from common.logs.logger import logger


class RabbitMQ:
    
    """this class holds all utility functions and variables for rabbitMQ message broker """
        
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

    def publish_message(self, exchange, routing_key, message, exchange_type="direct"):
        
        """Publish a message to an exchange."""
        
        try:
            self.connect()
            
            self.channel.exchange_declare(
                exchange=exchange, 
                exchange_type=exchange_type, 
                durable=True
                )
            
            self.channel.basic_publish(
                exchange=exchange,
                routing_key=routing_key,
                body=json.dumps(message),
                properties=pika.BasicProperties(delivery_mode=2)  # Persistent
            )
            logger.info(f"Broker Message to ['{exchange}'] - routing key['{routing_key}']-message-[{message['event_type']}]")
        
        except Exception as e:
            logger.error(f"Failed to publish message: {e}")
            
        finally:
            self.close_connection()
            

    def consume_messages(self, queue_name, callback):
        
        """Consume messages from a queue."""
        
        try:
            self.connect()
            
            self.channel.queue_declare(
                queue=queue_name, 
                durable=True
                )
            
            self.channel.basic_consume(
                queue=queue_name, 
                on_message_callback=callback, 
                auto_ack=True
                )
            
            print(f"Waiting for messages from queue '{queue_name}'. To exit press CTRL+C")
            
            self.channel.start_consuming()
            
        except Exception as e:
            print(f"Failed to consume messages: {e}")
            
        finally:
            self.close_connection()

    def bind_queue(self, queue_name, exchange, routing_key, exchange_type="direct"):
        
        """Bind a queue to an exchange."""
        
        try:
            self.connect()
            self.channel.exchange_declare(exchange=exchange, exchange_type=exchange_type, durable=True)
            self.channel.queue_declare(queue=queue_name, durable=True)
            self.channel.queue_bind(exchange=exchange, queue=queue_name, routing_key=routing_key)   
            print(f"Queue '{queue_name}' bound to exchange '{exchange}' with routing key '{routing_key}'")
            
        except Exception as e:
            
            print(f"Failed to bind queue to exchange: {e}")
            
        finally:
            
            self.close_connection()

    def close_connection(self):
    
        """Close the RabbitMQ connection."""

        if self.connection:
            self.connection.close()

