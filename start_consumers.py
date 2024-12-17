import os
import sys
import importlib
from common.message_broker.consumer_manager import start_consumer_processes
from common.logs.logger import logger

# Path to the services directory
SERVICES_DIR = os.path.join(os.path.dirname(__file__), "services")

def load_consumer_objects(service_name):
    
    """Dynamically load the consumer_objects module for a given service."""
    
    try:
        module_path = f"services.{service_name}.consumer_objects"
        consumer_module = importlib.import_module(module_path)
        return getattr(consumer_module, f"{service_name.upper()}_CONSUMERS", [])
    
    except ModuleNotFoundError:
        logger.warning(f"No consumer_objects.py found for service: {service_name}")
        return []
    
    except AttributeError as e:
        logger.error(f"Error loading consumers for service '{service_name}': {e}")
        return []

def start_all_consumers():
    """Start all consumers for all services."""
    services = [d for d in os.listdir(SERVICES_DIR) if os.path.isdir(os.path.join(SERVICES_DIR, d))]
    
    for service in services:
        logger.info(f"Starting consumers for service: {service}")
        consumers = load_consumer_objects(service)
        
        if consumers:
            start_consumer_processes(consumers=consumers)

if __name__ == "__main__":
    try:
        logger.info("Starting all message consumers...")
        start_all_consumers()
        
    except Exception as e:
        logger.error(f"Failed to start consumers: {e}")
