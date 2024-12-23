import os
from seed_database_functions import bulk_insert

# SERVICE 3
from services.service7_tasks_services.models import Task
from services.service7_tasks_services.app import app

if __name__ == "__main__":
    # Construct absolute path to mock data
    mock_data_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), '../mock_data/service7_task_data.json')
    )
    
    print(f"Resolved file path: {mock_data_path}")
    
    # Service 5: schedule
    bulk_insert(app, Task, mock_data_path, number_of_entries=10)