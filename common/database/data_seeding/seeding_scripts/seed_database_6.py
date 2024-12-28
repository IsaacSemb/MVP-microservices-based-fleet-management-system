import os
from seed_database_functions import bulk_insert

# SERVICE 3
from services.service6_fuel_consumption_service.models import FuelConsumption
from services.service6_fuel_consumption_service.app import app

if __name__ == "__main__":
    # Construct absolute path to mock data
    mock_data_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), '../mock_data/service6_fuel.json')
    )
    
    print(f"Resolved file path: {mock_data_path}")
    
    # Service 5: schedule
    bulk_insert(app, FuelConsumption, mock_data_path, number_of_entries=2)
