import os
import sys
import django
import random
from django.conf import settings

# Add the backend directory to Python path
backend_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
sys.path.insert(0, backend_path)

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'retrospectives.settings')

# Setup Django
django.setup()

import json
from ollama import chat
from ollama import ChatResponse
from typing import TypedDict
from api.models import Retrospective
from api.schemas import SYSTEM_PROMPT_GENERATE_ACTIONS

# RETROSPECTIVE_TITLE = "Mushroom Kingdom Retro #1"

class RetroItem(TypedDict):
    content: str
    category: str

def get_cards(retrospective_title: str) -> list[RetroItem]:
  retro = Retrospective.objects.get(title=retrospective_title)
  cards = retro.items.all()
  retro_items: list[RetroItem] = [{"content": card.content, "category": card.category} for card in cards]
  return retro_items


def get_action_items(retrospective_title: str) -> list[RetroItem]:

  response: ChatResponse = chat(model='mistral', messages=[
    {
      'role': 'system',
      'content': SYSTEM_PROMPT_GENERATE_ACTIONS,
    },
    {
        "role": "user",
        "content": f"Here are the retro items:\n{get_cards(retrospective_title)}"
    }
  ])
  try:
    return json.loads(response.message.content)
  except json.JSONDecodeError:
    print(f"Error parsing JSON: {response.message.content}")
    return []