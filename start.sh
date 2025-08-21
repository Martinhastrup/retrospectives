#!/bin/bash

# Start the backend
cd /app/backend
source /opt/venv/bin/activate

# Run migrations
python manage.py migrate

# Ensure database file has proper permissions after creation
if [ -f "db.sqlite3" ]; then
    chmod 666 db.sqlite3
    chown appuser:appuser db.sqlite3
fi

python manage.py runserver 0.0.0.0:8000 &

# Start the frontend (Vite dev server for hot reloading)
cd /app/frontend

# Create temp directories in locations where we have write permissions
mkdir -p /tmp/vite
mkdir -p /tmp/.vite

# Set environment variables for Vite development
export VITE_CACHE_DIR=/tmp/vite
export VITE_TEMP_DIR=/tmp/vite
export VITE_ROOT=/tmp
export NODE_ENV=development

# Start Vite with proper permissions and temp directory
VITE_CACHE_DIR=/tmp/vite npm run dev -- --host 0.0.0.0 --port 3000 &

# Wait for both processes
wait
