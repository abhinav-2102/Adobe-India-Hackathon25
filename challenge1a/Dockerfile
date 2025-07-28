# Use a specific, lightweight Python image.
# Explicitly set the platform to linux/amd64 as required by the challenge.
FROM --platform=linux/amd64 python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file first to leverage Docker cache
COPY requirements.txt .

# Install the dependencies
# --no-cache-dir reduces image size
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY main.py .

# This container is designed to be run with volume mounts for input and output.
# The CMD executes the Python script to process the files.
# The script is written to find PDFs in /app/input and write JSONs to /app/output.
CMD ["python", "main.py"]
