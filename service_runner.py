import os
import subprocess

# List of service directories and corresponding app.py files
SERVICES = [
    "service1_driver_management",
    "service2_vehicle_management",
    "service3_assignments",
    "service4_maintenance_repairs",
    "service5_scheduling",
    "service6_fuel_consumption_service",
    "service7_tasks_services"
]

BASE_DIR = 'c:/Users/ikesemb/Desktop/MASTERS PROJECT/001-DISSERTATION/000_proof_of_concept_stuff/MSA_ITERATION_3/services'
VENV_PYTHON = 'c:/Users/ikesemb/Desktop/MASTERS PROJECT/001-DISSERTATION/000_proof_of_concept_stuff/MSA_ITERATION_3/.venv/Scripts/python.exe'

def start_services(services_to_start):
    """Start the specified Flask services within the virtual environment."""
    processes = []

    for service in services_to_start:
        service_path = os.path.join(BASE_DIR, service, "app.py")
        if os.path.exists(service_path):
            # Use the virtual environment Python executable
            proc = subprocess.Popen([VENV_PYTHON, service_path])
            processes.append(proc)
            print(f"Started: {service}")
        else:
            print(f"Service app.py not found for: {service}")

    return processes

if __name__ == "__main__":
    print("Available services:")
    for idx, service in enumerate(SERVICES, start=1):
        print(f"{idx}. {service}")

    # Get user input for services to start
    service_indices = input("Enter the numbers of services to start (e.g., 1 2 3): ").split()
    
    try:
        # Map indices to service names
        services_to_start = [SERVICES[int(i) - 1] for i in service_indices]
    except (IndexError, ValueError):
        print("Invalid input. Please provide valid service numbers.")
        exit(1)

    print("Starting selected Flask services...")
    procs = start_services(services_to_start)

    try:
        input("Press Enter to stop services...\n")
    finally:
        # Ensure all processes are terminated
        for proc in procs:
            proc.terminate()
            proc.wait()  # Ensure proper cleanup
        print("All services stopped.")
