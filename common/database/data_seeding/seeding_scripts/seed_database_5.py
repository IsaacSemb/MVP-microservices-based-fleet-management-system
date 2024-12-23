import os
from seed_database_functions import bulk_insert

# SERVICE 3
from services.service5_scheduling.models import Schedule
from services.service5_scheduling.app import app

if __name__ == "__main__":
    # Construct absolute path to mock data
    mock_data_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), '../mock_data/service5_schedule_data.json')
    )
    
    print(f"Resolved file path: {mock_data_path}")
    
    # Service 5: schedule
    bulk_insert(app, Schedule, mock_data_path, number_of_entries=10)
