# Use Ubuntu 22.04 as the base image
FROM ubuntu:22.04

# Set environment variables
ENV PYTHONUNBUFFERED=1 

# Set the working directory
WORKDIR /app

# Install Python and any required libraries
RUN apt-get update && \
  apt-get install -y python3 python3-pip && \
  rm -rf /var/lib/apt/lists/*

# Copy the application files
COPY . /app

# Set the entry point for the logflow command
RUN chmod +x /app/main.py  # Make sure main.py is executable

# Expose any required ports
EXPOSE 514 40000 40001

# Run logflow with specified configuration
ENTRYPOINT ["python3", "/app/main.py"]

