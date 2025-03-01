# Step 1: Use an official Python image to build the app
FROM python:3.9-slim AS backend

# Step 2: Set the working directory inside the container
WORKDIR /AppBackend

# Install system dependencies required for mysqlclient and other Python packages
RUN apt-get update && apt-get install -y \
    pkg-config \
    libmariadb-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app code
COPY . .

# Expose the API port
EXPOSE 8000

# Command to run FastAPI app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
