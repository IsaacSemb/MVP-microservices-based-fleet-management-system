import os
from seed_database_functions import bulk_insert

# SERVICE 2
from services.service2_vehicle_management.models import Vehicle
from services.service2_vehicle_management.app import app

if __name__ == "__main__":
    # Construct absolute path to mock data
    mock_data_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), '../mock_data/service2_vehicle_data.json')
    )
    
    print(f"Resolved file path: {mock_data_path}")
    
    # Service 1: Driver Data
    bulk_insert(app, Vehicle, mock_data_path, number_of_entries=950)
