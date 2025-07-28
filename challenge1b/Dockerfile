# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
# --no-cache-dir ensures that we don't store the pip cache, which reduces image size
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application's code into the container at /app
COPY . .

# The main.py script expects 'input' and 'output' directories.
# We create them here to ensure the script can run without errors.
RUN mkdir -p /app/input /app/output

# Define the command to run your application
CMD ["python", "main.py"]
