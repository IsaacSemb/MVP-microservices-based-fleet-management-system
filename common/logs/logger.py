import logging
import os

# Create a logger instance
logger = logging.getLogger("fleet_management")
logger.setLevel(logging.DEBUG if os.getenv("FLASK_ENV") == "development" else logging.INFO)

# Create a console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

# Create a file handler
log_file = os.path.join(os.getcwd(), "fleet_management.log")
file_handler = logging.FileHandler(log_file)
file_handler.setLevel(logging.INFO)

# Define a logging format
formatter = logging.Formatter("[%(asctime)s]-[%(filename)s]-[%(levelname)s]-%(message)s")
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

# Add handlers to the logger
logger.addHandler(console_handler)
logger.addHandler(file_handler)
