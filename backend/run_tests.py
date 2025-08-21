#!/usr/bin/env python
"""
Simple test runner script for the retrospectives project.
This script runs pytest with the correct Django settings.
"""

import os
import sys
import django
from django.conf import settings

# Add the project directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'retrospectives.settings')

# Setup Django
django.setup()

if __name__ == '__main__':
    import pytest
    
    # Run pytest with Django settings
    sys.exit(pytest.main([
        '--tb=short',
        '--strict-markers',
        '-v',
        '--reuse-db',  # Reuse test database for faster runs
        '--nomigrations',  # Skip migrations in tests for speed
    ]))
