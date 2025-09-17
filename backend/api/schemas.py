"""
Shared Pydantic models and constants for the retrospective app.
This module contains common data structures used across multiple services.
"""

from pydantic import BaseModel
from typing import List, Optional


# =============================================================================
# Pydantic Models
# =============================================================================

class RetroItem(BaseModel):
    """Base model for retrospective items."""
    content: str
    category: str
    cluster_id: Optional[int] = None


class RetroItemList(BaseModel):
    """Container for a list of retrospective items."""
    retro_items: List[RetroItem]


# =============================================================================
# Constants
# =============================================================================

# AI Service Configuration
DEFAULT_OLLAMA_HOST = '127.0.0.1:11434'
DEFAULT_AI_MODEL = 'mistral'
DEFAULT_SENTENCE_TRANSFORMER = 'all-MiniLM-L6-v2'

# System Prompts
SYSTEM_PROMPT_GENERATE_ACTIONS = '''
You are a team leader for an agile retrospective.
Based on cards created by the team, provide actionable insights to improve the team's performance.

Rules:
- Read the retro items provided.
- RetroItem is a TypedDict defined as:
class RetroItem(TypedDict):
    content: str
    category: str
- category is always: 'actions'
- Output only valid JSON: a list of RetroItems.
- Output in the same language as the retro items.
- Group similar items together into a single item.
- Items MUST be based on the retro items provided.
- Limit output to maximum 7 items, but fewer are ok.
- Produce a list of new RetroItems.
- It should be possible to parse the output using json.loads(response.message.content)
'''

# Retrospective Categories
RETROSPECTIVE_CATEGORIES = [
    'start',
    'stop', 
    'good',
    'bad',
    'actions'
]

# User Roles
USER_ROLES = [
    'Admin',
    'Developer',
    'Observer'
]

# Retrospective Status
RETROSPECTIVE_STATUS = [
    'active',
    'completed',
    'archived'
]

# Action Item Status
ACTION_ITEM_STATUS = [
    'open',
    'in_progress',
    'completed',
    'cancelled'
]

# Action Item Priority
ACTION_ITEM_PRIORITY = [
    'low',
    'medium',
    'high',
    'urgent'
]
