from multiprocessing import Process
from common.message_broker.rabbitmq_utils import RabbitMQ
from common.logs.logger import logger

def start_consumer_processes(consumers=None):
    """
    Start multiple consumer processes.
    Args:
        consumers (list): List of consumer configurations, each with:
            queue_name,
            exchange,
            exchange_type,
            routing_key,
            handler
    """
    processes = []
    for consumer in consumers:
        process = Process(
            target=_start_single_consumer,
            args=(
                consumer["queue_name"],
                consumer["exchange"],
                consumer["exchange_type"],
                consumer["routing_key"],
                consumer["handler"],
            ),
            daemon=True,
        )
        processes.append(process)
        process.start()
    logger.info(f"Started {len(processes)} consumer processes.")

def _start_single_consumer(queue_name, exchange, exchange_type, routing_key, handler):
    """Start a single consumer."""
    rabbitmq = RabbitMQ()
    logger.info("binding queues")
    rabbitmq.bind_queue(queue_name, exchange, routing_key, exchange_type)
    
    logger.info('consumer has started')
    rabbitmq.consume_messages(queue_name, handler)
