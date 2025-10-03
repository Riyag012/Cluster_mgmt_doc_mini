# DOCKER
FROM apache/spark:latest

# Set the working directory for our application
WORKDIR /app

# Copy the application script and data files
COPY app.py .

# MINIKUBE

# FROM spark:latest

# # Set the working directory for our application
# WORKDIR /app

# # Copy the application script and data files
# COPY app.py .
# COPY data/ ./data/


