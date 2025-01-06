# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install dependencies from the requirements.txt file
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port the app runs on (if applicable)
EXPOSE 8000

# Define environment variables or start the application (if applicable)
CMD ["python3", "main.py"]