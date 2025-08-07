#!/bin/bash

# Start the backend
cd /app/backend
source /opt/venv/bin/activate
python manage.py migrate
python manage.py runserver 0.0.0.0:8000 &

# Start the frontend (serve built files using Python's HTTP server)
cd /app/frontend/dist
python3 -m http.server 3000 --bind 0.0.0.0 &

# Wait for both processes
wait
