FROM python:3.12

# Set the working directory to /app
# Copy the entire ../.. directory to /app
# Copy the requirements.txt from the root directory to /app
COPY ./ /app
#
# Set the working directory to /app
WORKDIR /app
#
# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
#
# # Expose the port the app runs on
EXPOSE 5000
#
# RUN python services/<<service_name>>/main.py
# Keep it alive
CMD ["python", "services/Ollama123/main.py"]
