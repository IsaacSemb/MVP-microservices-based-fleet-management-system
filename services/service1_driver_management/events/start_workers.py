import os
import sys

# Add the project root directory to sys.path
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
sys.path.append(root_path)

# Now import the shared module
from shared.message_broker.consumer_manager import start_consumer_processes
from consumer_objects import SERVICE_1_CONSUMERS
from shared.logs.logger import logger

if __name__ == "__main__":
    try:
        logger.info("Starting message consumers for Driver Management Service...")
        start_consumer_processes(consumers=SERVICE_1_CONSUMERS)
    except Exception as e:
        logger.error(f"Failed to start message consumers: {e}")
