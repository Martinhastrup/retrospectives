# Use Ubuntu 22.04 as the base image
FROM ubuntu:22.04

# Set environment variables to avoid interactive prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    curl \
    gnupg \
    software-properties-common \
    && rm -rf /var/lib/apt/lists/*

# Install Node.js 18.x
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs

# Copy requirements files first for better caching
COPY backend/requirements.txt ./backend/requirements.txt
COPY frontend/package.json ./frontend/package.json

# Install Python dependencies
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --upgrade pip && \
    pip install -r backend/requirements.txt

# Install Node.js dependencies
WORKDIR /app/frontend
RUN npm install

# Copy the rest of the application
WORKDIR /app
COPY . .

# Build the frontend (skip type checking for Docker build)
WORKDIR /app/frontend
RUN npm run build:docker

# Set up the backend
WORKDIR /app/backend

# Copy and set up the startup script before creating user
COPY start.sh /app/start.sh
RUN chmod +x /app/start.sh

# Create a non-root user for security
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app && \
    chmod -R 755 /app && \
    chmod -R 777 /app/frontend && \
    chmod -R 777 /app/frontend/node_modules && \
    mkdir -p /tmp/vite && \
    chown -R appuser:appuser /tmp/vite && \
    mkdir -p /app/frontend/.vite && \
    chown -R appuser:appuser /app/frontend/.vite && \
    chmod -R 777 /app/frontend/.vite && \
    # Ensure database directory has proper permissions
    mkdir -p /app/backend && \
    chmod -R 777 /app/backend && \
    chown -R appuser:appuser /app/backend

USER appuser

# Expose ports
EXPOSE 8000 3000

# Set the default command
CMD ["/app/start.sh"]
