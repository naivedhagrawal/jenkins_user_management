# Use a lightweight Python image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the application code
COPY jenkins_manager.py /app

# Install dependencies
RUN pip install PyQt5 requests

# Set the command to run the application
CMD ["python", "jenkins_manager.py"]
