# Dockerfile
FROM python:3.12-slim

WORKDIR /app

# install curl for healthcheck
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
      ffmpeg \
      fonts-dejavu-core \
      curl \
 && rm -rf /var/lib/apt/lists/*

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy FastAPI application
COPY main.py .

# Create folder for user scripts
RUN mkdir /app/code

# Expose HTTP port
EXPOSE 8000

# Healthcheck
HEALTHCHECK --start-period=15s CMD curl --fail http://localhost:8000/health || exit 1

# Start the FastAPI server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]
