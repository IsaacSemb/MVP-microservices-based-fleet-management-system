from jinja2 import Template
import os

# Define the Supervisor configuration template
supervisor_template = """
[supervisord]
nodaemon=true

[program:{{ service_name }}_flask]
command=python app.py
directory=/app/services/{{ service_name }}
autostart=true
autorestart=true

# log to the console
stdout_logfile=/dev/stdout
stderr_logfile=/dev/stderr
stdout_logfile_maxbytes=0
stderr_logfile_maxbytes=0

# log to a file
# stdout_logfile=/var/log/{{ service_name }}_workers_stdout.log
# stderr_logfile=/var/log/{{ service_name }}_workers_stderr.log
# stdout_logfile_maxbytes=10MB
# stderr_logfile_maxbytes=10MB
# stdout_logfile_backups=5
# stderr_logfile_backups=5




[program:{{ service_name }}_workers]
command=python events/workers.py
directory=/app/services/{{ service_name }}
autostart=true
autorestart=true

# log ot the console
stdout_logfile=/dev/stdout
stderr_logfile=/dev/stderr
stdout_logfile_maxbytes=0
stderr_logfile_maxbytes=0


# log to a file
# stdout_logfile=/var/log/{{ service_name }}_workers_stdout.log
# stderr_logfile=/var/log/{{ service_name }}_workers_stderr.log
# stdout_logfile_maxbytes=10MB
# stderr_logfile_maxbytes=10MB
# stdout_logfile_backups=5
# stderr_logfile_backups=5
"""

# Define service-specific data
services = [
    {"service_name": "service1_driver_management"},
    {"service_name": "service2_vehicle_management"},
    {"service_name": "service3_assignments"},
    {"service_name": "service4_maintenance_repairs"},
    {"service_name": "service5_scheduling"},
    {"service_name": "service6_fuel_consumption_service"},
    {"service_name": "service7_tasks_services"},
]

# Generate Supervisor configurations for each service
template = Template(supervisor_template)

for service in services:
    # Render the template with service-specific data
    supervisor_content = template.render(service_name=service["service_name"])
    
    # Define the output directory for the service
    service_dir = f"./services/{service['service_name']}"
    os.makedirs(service_dir, exist_ok=True)
    
    # Write the Supervisor configuration to the service directory
    with open(f"{service_dir}/supervisord.conf", "w") as f:
        f.write(supervisor_content)
    
    print(f"Supervisor configuration created for {service['service_name']} at {service_dir}/supervisord.conf")
