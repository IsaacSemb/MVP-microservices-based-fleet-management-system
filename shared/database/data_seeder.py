import sys
import os
import json
from dotenv import load_dotenv

# Load the correct environment file based on FLASK_ENV_FILE
# Default to `.env.local` if FLASK_ENV_FILE is not set
env_file = os.getenv('FLASK_ENV_FILE', '.env.local')
load_dotenv(env_file)

# Add the service directory to sys.path so Python knows where to find models and utils
service_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(service_path)

# Correct import statements
from models.vehicle_model import Vehicle
from utils.bulk_insert_utils import bulk_insert
from app import app  # Import the Flask app to get the context

# Load data from JSON file in the scripts folder
json_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sample_data.json')
try:
    with open(json_file_path, 'r') as file:
        vehicles = json.load(file)
except FileNotFoundError:
    print(f"Error: The file {json_file_path} was not found. Make sure the JSON file is in the correct location.")
    sys.exit(1)

# Use the app context when interacting with the database
with app.app_context():
    bulk_insert(Vehicle, vehicles)
