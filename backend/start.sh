#!/bin/bash

# Install dependencies if requirements.txt is newer than installed packages
pip install -r requirements.txt

# Run database migrations
python manage.py migrate

# Start the development server
python manage.py runserver 0.0.0.0:8000 