# validation_utils.py
import requests

def validate_and_fetch_resource( url, resource_id):

    """
    Validates if a resource (e.g., driver, vehicle) exists by hitting the service endpoint.
    Returns a tuple of (boolean, response_code, resource details) where the boolean indicates if the resource exists.
    If the resource exists, the response will contain the resource data; otherwise, an error message.
    """

    resource_url = f"{url}/{resource_id}"
    response = requests.get(resource_url)
    
    if response.status_code != 200:
        return False, response.status_code, None
    
    return True, response.status_code, response.json()