# MVP Microservices-Based Fleet Management System

Welcome to the MVP Microservices-Based Fleet Management System! This project is part of a dissertation aimed at demonstrating the viability of using a **microservices architecture** as opposed to a monolithic architecture. The project is also designed for personal learning and future advancements.

## Services Overview

The following microservices have been included in this project: 

1. **Driver Service**  
   - Stores driver details.
   - Manages driver-related logic, such as availability.

2. **Vehicle Service**  
   - Stores vehicle data.
   - Handles vehicle-related logic, including availability.

3. **Assignment Service**  
   - Manages the logic of assigning drivers to vehicles.
   - Handles sorting of driver and vehicle availability.

4. **Maintenance Service**  
   - Responsible for routine maintenance, repairs, and predictive maintenance logic.

5. **Scheduling Service**  
   - Builds schedules for all timeline operations.

6. **Fuel Consumption Service**  
   - Manages and logs fuel consumption and related data.

7. **Tasks Service**  
   - Manages all granular tasks carried out daily by the fleet.

**More services and features may be added in the future as the project evolves.**

---

## Prerequisites

1. **Git**: Ensure Git is installed on your machine.
2. **Docker Desktop**: Install Docker Desktop from [here](https://www.docker.com/products/docker-desktop/).

---

## Getting Started

### 1. Clone the Repository

Pull the project repository from GitHub by running the following command in your terminal:

```bash
git clone https://github.com/IsaacSemb/MVP-microservices-based-fleet-management-system.git
```

### 2. Navigate to the Project Folder

Change into the project directory:

```bash
cd MVP-microservices-based-fleet-management-system
```

### 3. Start the Application

Build and start the Docker containers using:

```bash
docker-compose up --build
```

### 4. Access the API Documentation

Once the application is running, open your browser and navigate to:

[http://localhost:8000/docs/](http://localhost:8000/docs/)

This link provides access to the API documentation and available endpoints.

---

## Notes

- Ensure Docker Desktop is running before executing the `docker-compose` commands.
- If you encounter any issues, ensure your Docker environment is set up correctly and consult the logs output from the terminal.

---

That's it! You're ready to interact with the Fleet Management System APIs. 🚀
