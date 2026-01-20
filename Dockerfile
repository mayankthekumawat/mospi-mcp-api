# FastMCP 2.0 Production Dockerfile
FROM python:3.11-slim

# Set working directory inside the container
WORKDIR /app

# Prevent Python from writing .pyc files and buffering stdout
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies (needed for pandas/numpy/openpyxl)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the server code and the dataset folder
COPY mospi_server.py .
COPY mospi/ ./mospi/

# Expose the port for HTTP transport
EXPOSE 8000

# Run the server using FastMCP CLI with HTTP transport
# FastMCP 2.0 handles the web server internally
CMD ["fastmcp", "run", "mospi_server.py:mcp", "--transport", "http", "--port", "8000", "--host", "0.0.0.0"]
