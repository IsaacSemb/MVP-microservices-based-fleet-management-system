import os
from seed_database_functions import bulk_insert

# SERVICE 1
from services.service1_driver_management.models import Driver
from services.service1_driver_management.app import app

if __name__ == "__main__":
    # Construct absolute path to mock data
    mock_data_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), '../mock_data/service1_driver_data.json')
    )
     
    print(f"Resolved file path: {mock_data_path}")
    
    # Service 1: Driver Data 
    bulk_insert(app, Driver, mock_data_path, number_of_entries=950)