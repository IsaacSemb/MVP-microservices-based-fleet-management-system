# run_all_seeds.py
import subprocess, sys

services = [
    "seed_database_1.py",
    # "seed_database_2.py",
    # "seed_database_3.py",
    # "seed_database_4.py",
    # "seed_database_5.py",
    # "seed_database_6.py",
    # "seed_database_7.py",
]

def run_seeding():
    
    # Dynamically determine the Python interpreter being used
    python_executable = sys.executable  # Gets the path to the current Python executable
    
    print("CURRENT ENVIRONMENT EXCECUTABLE")
    print(python_executable)

    for service in services:
        try:
            print(f"Running {service}...")
            # subprocess.run(["c:/Users/ikesemb/Desktop/MASTERS PROJECT/001-DISSERTATION/000_proof_of_concept_stuff/MSA_ITERATION_3/.venv/Scripts/python.exe", f"common/database/data_seeding/seeding_scripts/{service}"], check=True)
            subprocess.run([python_executable, f"common/database/data_seeding/seeding_scripts/{service}"], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error seeding {service}: {e}")

if __name__ == "__main__":
    run_seeding()