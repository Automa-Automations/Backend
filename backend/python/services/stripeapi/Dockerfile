FROM python:3.12

# Set the working directory to /app
# Copy the entire ../.. directory to /app
COPY ../../ /app

# Set the working directory to /app
WORKDIR /app

# Install any needed packages specified in requirements.txt
pip install --no-cache-dir -r requirements.txt

# Expose the port the app runs on
EXPOSE <<PORT>>

python services/<<SERVICE_NAME>>/main.py
