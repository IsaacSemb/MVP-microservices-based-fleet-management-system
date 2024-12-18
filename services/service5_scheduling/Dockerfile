
# Step 1: Use an official Python runtime
FROM python:3.12-slim

# Step 2: Set the working directory inside the container
WORKDIR /app

# Step 3: Install required system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libmariadb-dev \
    pkg-config \
    supervisor \
    && rm -rf /var/lib/apt/lists/*

# Step 4: Copy the 'common' directory into the container
COPY ./common /app/common

# Step 5: Copy the specific service directory into its correct path
RUN mkdir -p /app/services
COPY ./services/service5_scheduling /app/services/service5_scheduling

# Step 6: Copy requirements.txt from the project root
COPY ./requirements.txt /app/requirements.txt

# Step 7: Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Step 8: Expose the correct port
EXPOSE 5005

# Step 9: Copy supervisor configuration
COPY ./services/service5_scheduling/supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Step 10: Use supervisor as the entrypoint
CMD ["supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]