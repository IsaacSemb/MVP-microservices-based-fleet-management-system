import yaml
import json
import os

# Read the YAML file

yaml_file = os.path.abspath(
        os.path.join(os.path.dirname(__file__), './message_map.yml')
    )

destination_json_file = os.path.abspath(
        os.path.join(os.path.dirname(__file__), './message_map.json')
    )

with open(yaml_file, 'r') as file:
    yaml_data = yaml.safe_load(file)

# Convert YAML data to JSON
json_data = json.dumps(yaml_data, indent=4)

# Save the JSON data to a file
json_file = destination_json_file  # Replace with your desired JSON file path
with open(json_file, 'w') as file:
    file.write(json_data)

print("Conversion complete! JSON data saved to", json_file)
