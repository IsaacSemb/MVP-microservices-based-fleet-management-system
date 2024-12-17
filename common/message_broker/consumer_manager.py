from multiprocessing import Process
from common.message_broker.rabbitmq_utils import RabbitMQ
from common.logs.logger import logger


def start_consumer_processes(consumers=None):
    """
    Start multiple consumer processes.
    Args:
        consumers (list): List of consumer configurations.
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
        )  # Do not set daemon=True
        processes.append(process)
        process.start()
    logger.info(f"Started {len(processes)} consumer processes.")

    # Wait for processes to complete
    for process in processes:
        process.join()


def _start_single_consumer(queue_name, exchange, exchange_type, routing_key, handler):
    """Start a single consumer."""
    rabbitmq = RabbitMQ()
    try:
        rabbitmq.bind_queue(queue_name, exchange, routing_key, exchange_type)
        logger.info(f"Consumer for queue '{queue_name}' started.")
        rabbitmq.consume_messages(queue_name, handler)
    except Exception as e:
        logger.error(f"Consumer for queue '{queue_name}' encountered an error: {e}")
    finally:
        rabbitmq.close_connection()
