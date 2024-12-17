import os
import sys

# Adding project root directory to sys.path
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
sys.path.append(root_path)

from common.worker_manager.worker_manager import start_service_workers
from consumer_objects import SERVICE_6_CONSUMERS

if __name__ == '__main__':
    start_service_workers(SERVICE_6_CONSUMERS)
