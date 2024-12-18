from jinja2 import Template
import os

# Define the template
dockerfile_template = """
# Step 1: Use an official Python runtime
FROM python:3.12-slim

# Step 2: Set the working directory inside the container
WORKDIR /app

# Step 3: Install required system dependencies
RUN apt-get update && apt-get install -y \\
    gcc \\
    libmariadb-dev \\
    pkg-config \\
    supervisor \\
    && rm -rf /var/lib/apt/lists/*

# Step 4: Copy the 'common' directory into the container
COPY ./common /app/common

# Step 5: Copy the specific service directory into its correct path
RUN mkdir -p /app/services
COPY ./services/{{ service_name }} /app/services/{{ service_name }}

# Step 6: Copy requirements.txt from the project root
COPY ./requirements.txt /app/requirements.txt

# Step 7: Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Step 8: Expose the correct port
EXPOSE {{ service_port }}

# Step 9: Copy supervisor configuration
COPY ./services/{{ service_name }}/supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Step 10: Use supervisor as the entrypoint
CMD ["supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
"""

# Define service-specific data
services = [
    {"service_name": "service1_driver_management", "service_port": 5001},
    {"service_name": "service2_vehicle_management", "service_port": 5002},
    {"service_name": "service3_assignments", "service_port": 5003},
    {"service_name": "service4_maintenance_repairs", "service_port": 5004},
    {"service_name": "service5_scheduling", "service_port": 5005},
    {"service_name": "service6_fuel_consumption_service", "service_port": 5006},
    {"service_name": "service7_tasks_services", "service_port": 5007},
]

# Generate Dockerfiles for each service
template = Template(dockerfile_template)

for service in services:
    # Render the template with service-specific data
    dockerfile_content = template.render(
        service_name=service["service_name"],
        service_port=service["service_port"]
    )
    
    # Define the output directory for the service
    service_dir = f"./services/{service['service_name']}"
    os.makedirs(service_dir, exist_ok=True)
    
    # Write the Dockerfile to the service directory
    with open(f"{service_dir}/Dockerfile", "w") as f:
        f.write(dockerfile_content)
    
    print(f"Dockerfile created for {service['service_name']} at {service_dir}/Dockerfile")
