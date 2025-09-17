import json
import logging
import os
from typing import List
from ollama import Client
from api.models import Retrospective, RetrospectiveItem, User
from api.schemas import RetroItem, RetroItemList, SYSTEM_PROMPT_GENERATE_ACTIONS, DEFAULT_OLLAMA_HOST, DEFAULT_AI_MODEL

logger = logging.getLogger(__name__)


class GenAIService:
    """Service for generating action items using AI."""
    
    def __init__(self, model: str = DEFAULT_AI_MODEL, ollama_host: str = None):
        self.model = model
        self.ollama_host = ollama_host or os.environ.get('OLLAMA_HOST', DEFAULT_OLLAMA_HOST)
    
    def get_retrospective_items(self, retrospective_id: int) -> List[RetroItem]:
        """Get all items from a retrospective."""
        try:
            retrospective = Retrospective.objects.get(id=retrospective_id)
            items = retrospective.items.all()

            return [
                RetroItem(
                    category=item.category,
                    content=item.content,
                )
                for item in items
            ]
        except Retrospective.DoesNotExist:
            raise ValueError(f"Retrospective with id {retrospective_id} not found")
    
    def generate_retrospective_items(self, retrospective_id: int) -> List[RetroItem]:
        """Generate action items for a retrospective using AI."""
        try:
            # Get retrospective items
            retro_items = self.get_retrospective_items(retrospective_id)

            if not retro_items:
                logger.warning(f"No items found for retrospective {retrospective_id}")
                return []

            # Prepare the prompt
            items_text = "\n".join([
                f"- {item.category.upper()}: {item.content}"
                for item in retro_items
            ])

            user_prompt = f"Here are the retrospective items:\n\n{items_text}\n\nPlease generate actionable items to improve team performance."

            # Call Ollama
            # Set the Ollama host for this request
            original_host = os.environ.get('OLLAMA_HOST')
            os.environ['OLLAMA_HOST'] = self.ollama_host
            
            try:
                # Import ollama client here to ensure it picks up the environment variable
                from ollama import Client
                client = Client(host=self.ollama_host)

                response = client.chat(
                    model=self.model,
                    messages=[
                        {'role': 'system', 'content': SYSTEM_PROMPT_GENERATE_ACTIONS},
                        {'role': 'user', 'content': user_prompt}
                    ],
                    format=RetroItemList.model_json_schema(),
                )
            finally:
                # Restore original host setting
                if original_host is not None:
                    os.environ['OLLAMA_HOST'] = original_host
                elif 'OLLAMA_HOST' in os.environ:
                    del os.environ['OLLAMA_HOST']

            # Parse the response
            try:
                # Handle both dict and object response formats
                if isinstance(response, dict):
                    content = response['message']['content']
                else:
                    content = response.message.content
                
                retro_item_dict = RetroItemList.model_validate_json(content)
                return retro_item_dict.retro_items
            except (json.JSONDecodeError, KeyError, AttributeError) as e:
                logger.error(f"Failed to parse AI response as RetroItems: {e}")
                logger.error(f"AI response type: {type(response)}")
                logger.error(f"AI response: {response}")
                if isinstance(response, dict):
                    logger.error(f"AI response content: {response.get('message', {}).get('content', 'No content found')}")
                else:
                    logger.error(f"AI response content: {getattr(response, 'message', {}).content if hasattr(response, 'message') else 'No message attribute'}")
                raise ValueError("AI response is not valid JSON")
                
        except Exception as e:
            logger.error(f"Error generating action items: {e}")
            raise
    

    def create_retrospective_items_from_ai(self, retrospective_id: int) -> List[RetrospectiveItem]:
        """Generate and create retrospective items in the database."""
        try:
            # Generate retrospective items using AI
            ai_retrospective_items = self.generate_retrospective_items(retrospective_id)
            
            if not ai_retrospective_items:
                return []
            
            author = User.objects.filter(username="gen_ai_serviceuser").first()

            # Create RetrospectiveItem objects
            created_items = []
            retrospective = Retrospective.objects.get(id=retrospective_id)
            
            for index, item_data in enumerate(ai_retrospective_items):
                # Create organized grid layout for action items
                
                # Spacing for organized layout - different for minimized vs maximized
                min_x_spacing = 100  # Horizontal spacing
                max_x_spacing = 50  # Horizontal spacing
                
                retrospective_item = RetrospectiveItem.objects.create(
                    retrospective=retrospective,
                    content=item_data.content,
                    category=item_data.category,
                    x_minimized=index * min_x_spacing,
                    y_minimized=0,
                    x_maximized=index * max_x_spacing,
                    y_maximized=0,
                    author=author,
                )
                created_items.append(retrospective_item)
            
            logger.info(f"Created {len(created_items)} retrospective items for retrospective {retrospective_id}")
            return created_items
            
        except Exception as e:
            logger.error(f"Error creating retrospective items: {e}")
            raise
