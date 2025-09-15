#!/usr/bin/env python
"""
Script to update existing retrospective items with new coordinate ranges.
This ensures all items are visible in both minimized and expanded views.
"""

import os
import sys
import django
import random
from django.conf import settings

# Add the backend directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'retrospectives.settings')

# Setup Django
django.setup()

from api.models import RetrospectiveItem

def update_item_coordinates():
    """Update all retrospective items with new coordinate ranges."""
    print("🔄 Updating retrospective item coordinates...")
    
    # New coordinate ranges (for expanded squares, will be scaled down by frontend)
    min_x, max_x = 50, 500  # X range for expanded squares (will be scaled down)
    min_y, max_y = 50, 400  # Y range for expanded squares (will be scaled down)
    
    items = RetrospectiveItem.objects.all()
    updated_count = 0
    
    for item in items:
        # Generate new random coordinates
        new_x = random.randint(min_x, max_x)
        new_y = random.randint(min_y, max_y)
        
        # Update the item
        item.x = new_x
        item.y = new_y
        item.save()
        
        updated_count += 1
        print(f"✅ Updated item {item.id}: {item.category} - ({new_x}, {new_y})")
    
    print(f"\n✨ Updated {updated_count} retrospective items with new coordinates!")
    print(f"📏 New coordinate ranges: X({min_x}-{max_x}), Y({min_y}-{max_y})")

if __name__ == "__main__":
    update_item_coordinates()
