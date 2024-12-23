import os
from seed_database_functions import bulk_insert

# SERVICE 3
from services.service4_maintenance_repairs.models import MaintenanceLog
from services.service4_maintenance_repairs.app import app

if __name__ == "__main__":
    # Construct absolute path to mock data
    mock_data_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), '../mock_data/service4_maintenance.json')
    )
    
    print(f"Resolved file path: {mock_data_path}")
    
    # Service 3: Assignment Data
    bulk_insert(app, MaintenanceLog, mock_data_path, number_of_entries=10)
