"""
Script to create demo data for the retrospective app.
Will create a bunch of users, teams, and retrospectives.
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

from api.models import User, Team, Retrospective, RetrospectiveItem

def create_test_users() -> None:
    """Create a bunch of test users."""
    print("🛠️ Creating demo users...")
    
    users_data = [
        {
            "username": "Mario",
            "userfullname": "Super Mario",
            "email": "Mario@super.com",
            "role": 'Developer',
            "password": "testpass123",
        },
        {
            "username": "Luigi",
            "userfullname": "Super Luigi",
            "email": "Luigi@super.com",
            "role": 'Developer',
            "password": "testpass123",
        },
        {
            "username": "Toad",
            "userfullname": "Captain Toad",
            "email": "Toad@super.com",
            "role": 'Observer',
            "password": "testpass123",
        },
        {
            "username": "Peach",
            "userfullname": "Princess Peach",
            "email": "Peach@super.com",
            "role": 'Admin',
            "password": "testpass123",
        },
        {
            "username": "Yoshi",
            "userfullname": "Yoshi the Dinosaur",
            "email": "Yoshi@super.com",
            "role": 'Developer',
            "password": "testpass123",
        },
        {
            "username": "Bowser",
            "userfullname": "King Bowser sr.",
            "email": "BowserSR@super.com",
            "role": 'Developer',
            "password": "testpass123",
        },
        {
            "username": "Bowser Jr.",
            "userfullname": "Prince Bowser jr.",
            "email": "BowserJR@super.com",
            "role": 'Developer',
            "password": "testpass123",
        },
        {
            "username": "Wario",
            "userfullname": "Super Wario",
            "email": "Wario@super.com",
            "role": 'Developer',
            "password": "testpass123",
        },
        {
            "username": "Koopa",
            "userfullname": "Koopa the Turtle",
            "email": "Koopa@super.com",
            "role": 'Observer',
            "password": "testpass123",
        },
    ]
    
    for user_data in users_data:
        user, created = User.objects.get_or_create(
            username=user_data["username"],
            defaults={
                "userfullname": user_data["userfullname"],
                "email": user_data["email"],
                "role": user_data["role"],
            }
        )
        if created:
            user.set_password(user_data["password"])
            user.save()
            print(f"✅ Created user: {user.username}")
        else:
            print(f"⏭️ User already exists: {user.username}")

def create_test_teams() -> None:
    """Create a bunch of test teams."""
    print("🛠️ Creating demo teams...")
    
    team, created = Team.objects.get_or_create(
        name="Mushroom Kingdom",
        defaults={
            "description": "All things toads and turtles.",
        }
    )
    
    if created:
        # Add members to the newly created team
        team.members.set([
            User.objects.get(username="Mario"),
            User.objects.get(username="Luigi"),
            User.objects.get(username="Toad"),
            User.objects.get(username="Peach"),
            User.objects.get(username="Yoshi"),
            User.objects.get(username="Bowser"),
            User.objects.get(username="Bowser Jr."),
            User.objects.get(username="Wario"),
            User.objects.get(username="Koopa")
        ])
        print(f"✅ Created team: {team.name}")
    else:
        print(f"⏭️ Team already exists: {team.name}")

def create_test_retrospectives() -> None:
    """Create a bunch of test retrospectives."""
    print("🛠️ Creating demo retrospectives...")
    
    retrospectives_data = [
        {
            "title": "Mushroom Kingdom Retro",
            "description": "Retrospective for the Mushroom Kingdom team.",
        }
    ]
    
    team = Team.objects.get(name="Mushroom Kingdom")
    created_by = User.objects.get(username="Peach")
    
    for retro_data in retrospectives_data:
        retrospective, created = Retrospective.objects.get_or_create(
            title=retro_data["title"],
            defaults={
                "description": retro_data["description"],
                "team": team,
                "created_by": created_by,
            }
        )
        if created:
            print(f"✅ Created retrospective: {retrospective.title}")
        else:
            print(f"⏭️ Retrospective already exists: {retrospective.title}")

def create_test_retrospective_items() -> None:
    """Create a bunch of test retrospective items."""
    print("🎨 Creating demo retrospective items...")
    
    retro1_items = [
        # Good items (25)
        {
            "category": 'good',
            "content": "Successfully rescued Princess Peach from Bowser's castle",
            "author": "Mario",
        },
        {
            "category": 'good',
            "content": "Implemented new power-up system with fire flowers and stars",
            "author": "Luigi",
        },
        {
            "category": 'good',
            "content": "Built excellent castle security with moving platforms",
            "author": "Bowser",
        },
        {
            "category": 'good',
            "content": "Created beautiful mushroom kingdom landscapes",
            "author": "Toad",
        },
        {
            "category": 'good',
            "content": "Developed smooth jumping mechanics for all characters",
            "author": "Yoshi",
        },
        {
            "category": 'good',
            "content": "Designed challenging but fair level progression",
            "author": "Peach",
        },
        {
            "category": 'good',
            "content": "Implemented excellent sound effects and music",
            "author": "Bowser Jr.",
        },
        {
            "category": 'good',
            "content": "Created diverse enemy types with unique behaviors",
            "author": "Wario",
        },
        {
            "category": 'good',
            "content": "Built reliable save system for player progress",
            "author": "Koopa",
        },
        {
            "category": 'good',
            "content": "Designed intuitive controls that feel responsive",
            "author": "Mario",
        },
        {
            "category": 'good',
            "content": "Created memorable boss battles with unique patterns",
            "author": "Luigi",
        },
        {
            "category": 'good',
            "content": "Implemented excellent collision detection system",
            "author": "Bowser",
        },
        {
            "category": 'good',
            "content": "Built comprehensive tutorial system for new players",
            "author": "Toad",
        },
        {
            "category": 'good',
            "content": "Created vibrant color palette that's easy on the eyes",
            "author": "Yoshi",
        },
        {
            "category": 'good',
            "content": "Implemented smooth camera following system",
            "author": "Peach",
        },
        {
            "category": 'good',
            "content": "Designed excellent level variety with different themes",
            "author": "Bowser Jr.",
        },
        {
            "category": 'good',
            "content": "Created engaging multiplayer modes",
            "author": "Wario",
        },
        {
            "category": 'good',
            "content": "Built robust physics engine for realistic movement",
            "author": "Koopa",
        },
        {
            "category": 'good',
            "content": "Implemented excellent particle effects for power-ups",
            "author": "Mario",
        },
        {
            "category": 'good',
            "content": "Created memorable character animations and expressions",
            "author": "Luigi",
        },
        {
            "category": 'good',
            "content": "Designed excellent level editor for community content",
            "author": "Bowser",
        },
        {
            "category": 'good',
            "content": "Implemented smooth transitions between levels",
            "author": "Toad",
        },
        {
            "category": 'good',
            "content": "Created excellent achievement system for player engagement",
            "author": "Yoshi",
        },
        {
            "category": 'good',
            "content": "Built comprehensive analytics system for level design",
            "author": "Peach",
        },
        {
            "category": 'good',
            "content": "Implemented excellent accessibility features for all players",
            "author": "Bowser Jr.",
        },
        
        # Bad items (20)
        {
            "category": 'bad',
            "content": "Bowser keeps kidnapping Princess Peach every week",
            "author": "Mario",
        },
        {
            "category": 'bad',
            "content": "Goombas are spawning in unexpected places causing chaos",
            "author": "Luigi",
        },
        {
            "category": 'bad',
            "content": "Fire bars in castle levels are too unpredictable",
            "author": "Bowser",
        },
        {
            "category": 'bad',
            "content": "Toad houses are giving out the same power-ups repeatedly",
            "author": "Toad",
        },
        {
            "category": 'bad',
            "content": "Yoshi's flutter jump sometimes doesn't work properly",
            "author": "Yoshi",
        },
        {
            "category": 'bad',
            "content": "Princess Peach's floating ability is inconsistent",
            "author": "Peach",
        },
        {
            "category": 'bad',
            "content": "Bowser Jr.'s paintbrush mechanics are glitchy",
            "author": "Bowser Jr.",
        },
        {
            "category": 'bad',
            "content": "Wario's shoulder charge breaks through unintended walls",
            "author": "Wario",
        },
        {
            "category": 'bad',
            "content": "Koopa shells sometimes get stuck in corners",
            "author": "Koopa",
        },
        {
            "category": 'bad',
            "content": "Mario's fireball power-up has limited range",
            "author": "Mario",
        },
        {
            "category": 'bad',
            "content": "Luigi's vacuum cleaner doesn't work on all ghost types",
            "author": "Luigi",
        },
        {
            "category": 'bad',
            "content": "Bowser's fire breath attack has inconsistent hit detection",
            "author": "Bowser",
        },
        {
            "category": 'bad',
            "content": "Toad's speed boost power-up wears off too quickly",
            "author": "Toad",
        },
        {
            "category": 'bad',
            "content": "Yoshi's egg throwing mechanics are hard to control precisely",
            "author": "Yoshi",
        },
        {
            "category": 'bad',
            "content": "Princess Peach's parasol float has limited duration",
            "author": "Peach",
        },
        {
            "category": 'bad',
            "content": "Bowser Jr.'s magic paintbrush runs out of paint too fast",
            "author": "Bowser Jr.",
        },
        {
            "category": 'bad',
            "content": "Wario's ground pound creates too much screen shake",
            "author": "Wario",
        },
        {
            "category": 'bad',
            "content": "Koopa's shell spin attack is hard to aim accurately",
            "author": "Koopa",
        },
        {
            "category": 'bad',
            "content": "Mario's wall jump timing is too strict for new players",
            "author": "Mario",
        },
        {
            "category": 'bad',
            "content": "Luigi's high jump is inconsistent on different surfaces",
            "author": "Luigi",
        },
        
        # Start doing items (15)
        {
            "category": 'start',
            "content": "Start implementing new power-up combinations",
            "author": "Mario",
        },
        {
            "category": 'start',
            "content": "Start creating underwater levels with swimming mechanics",
            "author": "Luigi",
        },
        {
            "category": 'start',
            "content": "Start building airship levels with moving platforms",
            "author": "Bowser",
        },
        {
            "category": 'start',
            "content": "Start designing puzzle levels that require teamwork",
            "author": "Toad",
        },
        {
            "category": 'start',
            "content": "Start implementing Yoshi's different colored variants",
            "author": "Yoshi",
        },
        {
            "category": 'start',
            "content": "Start creating Princess Peach's adventure mode",
            "author": "Peach",
        },
        {
            "category": 'start',
            "content": "Start building Bowser Jr.'s paint world levels",
            "author": "Bowser Jr.",
        },
        {
            "category": 'start',
            "content": "Start implementing Wario's treasure hunting mechanics",
            "author": "Wario",
        },
        {
            "category": 'start',
            "content": "Start creating Koopa's racing mini-games",
            "author": "Koopa",
        },
        {
            "category": 'start',
            "content": "Start designing boss rush mode for experienced players",
            "author": "Mario",
        },
        {
            "category": 'start',
            "content": "Start implementing Luigi's mansion ghost hunting levels",
            "author": "Luigi",
        },
        {
            "category": 'start',
            "content": "Start creating Bowser's castle defense mini-game",
            "author": "Bowser",
        },
        {
            "category": 'start',
            "content": "Start designing Toad's mushroom kingdom tour mode",
            "author": "Toad",
        },
        {
            "category": 'start',
            "content": "Start implementing Yoshi's island exploration levels",
            "author": "Yoshi",
        },
        {
            "category": 'start',
            "content": "Start creating Princess Peach's castle management game",
            "author": "Peach",
        },
        
        # Stop doing items (10)
        {
            "category": 'stop',
            "content": "Stop making levels that require pixel-perfect jumps",
            "author": "Mario",
        },
        {
            "category": 'stop',
            "content": "Stop creating invisible blocks that surprise players",
            "author": "Luigi",
        },
        {
            "category": 'stop',
            "content": "Stop designing boss battles that last over 10 minutes",
            "author": "Bowser",
        },
        {
            "category": 'stop',
            "content": "Stop placing power-ups in unreachable locations",
            "author": "Toad",
        },
        {
            "category": 'stop',
            "content": "Stop making Yoshi's flutter jump consume too much stamina",
            "author": "Yoshi",
        },
        {
            "category": 'stop',
            "content": "Stop creating levels that require memorization to complete",
            "author": "Peach",
        },
        {
            "category": 'stop',
            "content": "Stop designing enemies that are impossible to defeat",
            "author": "Bowser Jr.",
        },
        {
            "category": 'stop',
            "content": "Stop making Wario's ground pound break essential platforms",
            "author": "Wario",
        },
        {
            "category": 'stop',
            "content": "Stop creating Koopa shells that bounce infinitely",
            "author": "Koopa",
        },
        {
            "category": 'stop',
            "content": "Stop designing levels that require specific character abilities",
            "author": "Mario",
        },
    ]
    
    # Create items for the single retrospective
    retrospectives = [
        ("Mushroom Kingdom Retro", retro1_items),
    ]
    
    for retro_title, items_data in retrospectives:
        retrospective = Retrospective.objects.get(title=retro_title)
        
        for item_data in items_data:
            author = User.objects.get(username=item_data["author"])
            
            # Use a combination of fields to check for uniqueness
            item, created = RetrospectiveItem.objects.get_or_create(
                retrospective=retrospective,
                category=item_data["category"],
                content=item_data["content"],
                author=author,
                defaults={
                    "x_minimized": random.randint(2, 125),   # Random x position for minimized squares (2-238px)
                    "y_minimized": random.randint(2, 100),   # Random y position for minimized squares (2-158px)
                    "x_maximized": random.randint(2, 500),  # Random x position for maximized squares (50-500px)
                    "y_maximized": random.randint(2, 400),  # Random y position for maximized squares (50-400px)
                }
            )
            
            if created:
                print(f"✅ Created item: {item_data['category']} by {item_data['author']} in {retro_title}")
            else:
                print(f"⏭️ Item already exists: {item_data['category']} by {item_data['author']} in {retro_title}")

def create_demo_data() -> None:
    """Create all demo data for the retrospective app."""
    print("🚀 Starting demo data creation...")
    print("=" * 50)
    
    create_test_users()
    print()
    create_test_teams()
    print()
    create_test_retrospectives()
    print()
    create_test_retrospective_items()
    
    print("=" * 50)
    print("✨ Demo data creation completed!")

if __name__ == "__main__":
    create_demo_data()
