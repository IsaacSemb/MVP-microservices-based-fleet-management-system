import os
from seed_database_functions import bulk_insert

# SERVICE 3
from services.service3_assignments.models import Assignment
from services.service3_assignments.app import app

if __name__ == "__main__":
    # Construct absolute path to mock data
    mock_data_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), '../mock_data/service3_assignment_data.json')
    )
    
    print(f"Resolved file path: {mock_data_path}")
    
    # Service 3: Assignment Data
    bulk_insert(app, Assignment, mock_data_path, number_of_entries=2)
