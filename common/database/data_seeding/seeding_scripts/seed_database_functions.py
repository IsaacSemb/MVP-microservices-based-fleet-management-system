import random
from sqlalchemy.exc import SQLAlchemyError
import json
import random
import string
import re
import sys
import os


# Dynamically add project root to PYTHONPATH
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../'))
sys.path.append(project_root)

# Now imports will work
from common.database.db_utils import db



def generate_new_license(existing_licenses):
    """
    Generate a new license number in the format DXXXXXXXXXX.
    """
    while True:
        new_license = f"D{random.randint(10**9, 10**10 - 1)}"  # Generate a 10-digit number prefixed with 'D'
        if new_license not in existing_licenses:
            existing_licenses.add(new_license)
            return new_license

def generate_new_plate(existing_plate_numbers):
    """
    Generate a new plate_number plate number in the format ABC1234 (3 letters followed by 4 digits).
    """
    while True:
        # Generate a random plate_number plate in the format ABC1234
        new_plate_number = f"{''.join(random.choices(string.ascii_uppercase, k=3))}{random.randint(1000, 9999)}"
        if new_plate_number not in existing_plate_numbers:
            existing_plate_numbers.add(new_plate_number)
            return new_plate_number

def override_license_numbers(data_list):
    """
    Override all license_no values with new unique ones in the format DXXXXXXXXXX.
    """
    existing_licenses = set()
    for record in data_list:
        record['license_no'] = generate_new_license(existing_licenses)
    return data_list

def override_plate_numbers(data_list):
    """
    Override all reg_no values with new unique ones in the format ABC1234.
    """
    existing_plate_numbers = set()
    for record in data_list:
        record['reg_no'] = generate_new_plate(existing_plate_numbers)
    return data_list

def bulk_insert(app, model, filepath, number_of_entries=1000):
    """
    Insert multiple entries into the database using SQLAlchemy bulk_insert_mappings.
    Completely override all license_no or reg_no values with new unique ones.
    """
    with app.app_context():
        try:
            
            # Clear the table before inserting new data
            db.session.query(model).delete()
            db.session.commit()
            print(f"Cleared all records from {model.__tablename__} table.")
        
            with open(filepath, 'r') as file:
                data_list = json.load(file)

            # Determine data type based on the file path using regex
            if re.search(r'service1', filepath, re.IGNORECASE):
                # Handle driver data
                print("Detected service1: Processing driver data")
                data_list = override_license_numbers(data_list)
            elif re.search(r'service2', filepath, re.IGNORECASE):
                # Handle vehicle data
                print("Detected service2: Processing vehicle data")
                data_list = override_plate_numbers(data_list)

            # Limit number of entries to 1000
            if number_of_entries >= len(data_list):
                number_of_entries = len(data_list) - 1 
            
                
            

            # Slice the list to the required number of entries
            data_list = data_list[:number_of_entries]

            # Using bulk_insert_mappings to insert multiple records
            db.session.bulk_insert_mappings(model, data_list)
            db.session.commit()
            print(f"Data successfully inserted into {model.__tablename__} table.")
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Error occurred: {e}")
        except FileNotFoundError:
            print("File not found. Please check the file path.")
        except json.JSONDecodeError:
            print("Error decoding JSON. Ensure the file format is correct.")

