import requests
import time
import uuid
import json
import os ,sys

def load_data_from_json(file_path):
    """
    Loads data from a JSON file.
    :param file_path: Path to the JSON file.
    :return: Data loaded from the JSON file as a list.
    """
    with open(file_path, "r") as file:
        return json.load(file)

def send_post_requests(data_list, url):
    """
    Sends each item in the list as an individual HTTP POST request to the specified URL,
    measuring the time taken for each request and the total time.
    """
    total_time = 0  # Initialize total time
    
    for i, driver in enumerate(data_list):
        try:
            start_time = time.time()  # Start timing the request
            
            # Assign UUIDs for driver_id and license_no
            driver["driver_id"] = str(uuid.uuid4())
            driver["license_no"] = str(uuid.uuid4())
            
            # Send POST request
            response = requests.post(url, json=driver)
            
            end_time = time.time()  # End timing the request
            elapsed_time = end_time - start_time  # Calculate elapsed time for the request
            
            print(f"Request {i+1}: Status Code: {response.status_code}, Response: {response.text}, Time: {elapsed_time:.4f} seconds")
            
            total_time += elapsed_time  # Add elapsed time to the total
            
        except Exception as e:
            print(f"Request {i+1}: An error occurred: {e}")
        
        # Limit requests 
        if i == 3:  
            break

    print(f"Total time for sending {i+1} requests: {total_time:.4f} seconds")

if __name__ == "__main__":
    # Path to the JSON file containing the driver data
    
     # Construct absolute path to mock data
    current_relative_path_to_target = '../../common/database/data_seeding//mock_data/service1_driver_data.json'
    data_path = os.path.abspath( os.path.join(os.path.dirname(__file__) , current_relative_path_to_target) )
     
    print(f"Resolved file path: {data_path}")
    json_file_path = data_path
    
    # Define the endpoint URL
    url = "http://localhost:5001/drivers"  # Adjust to your actual API endpoint
    
    # Load data from the JSON file
    data = load_data_from_json(json_file_path)
    
    # Send each driver as a separate POST request
    send_post_requests(data, url)
