# Use the official Python 3.9 slim image as the base
FROM python:3.9-slim

# Set the maintainer for the image
LABEL maintainer="tompots"

# Set working directory inside the container
WORKDIR /app

# Copy the dependencies file (requirements.txt) to the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project to the container
COPY . .

# Expose port (optional, if API or web server is used)
EXPOSE 8080

# Set the default command to run the main orchestrator script
CMD ["python", "ai_pipeline_orchestrator.py"]
