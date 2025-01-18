# Use official Python image as the base
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy the application code and model
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port for the app
EXPOSE 8000

# Command to run the app using Gunicorn with WSGI middleware
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "app:app_wsgi"]
