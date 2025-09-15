# GenAI Action Items API

This document describes the new GenAI-powered action item generation feature for retrospectives.

## Overview

The GenAI Action Items API allows you to automatically generate actionable items based on the content of a retrospective. It uses Ollama with the Mistral model to analyze retrospective items and suggest specific, actionable improvements.

## API Endpoint

### Generate Action Items

**POST** `/api/retrospectives/{id}/generate_action_items/`

Generates action items for a specific retrospective using AI analysis.

#### Parameters

- `id` (path parameter): The ID of the retrospective

#### Request Body

No request body required.

#### Response

**Success (201 Created):**
```json
{
    "message": "Successfully generated 3 action items",
    "action_items": [
        {
            "id": 1,
            "title": "Implement daily standup meetings",
            "description": "Set up a daily 15-minute standup meeting to improve team communication and alignment.",
            "status": "open",
            "priority": "medium",
            "assigned_to": null,
            "due_date": null,
            "created_at": "2024-01-15T10:30:00Z",
            "completed_at": null
        },
        {
            "id": 2,
            "title": "Create meeting agenda templates",
            "description": "Develop standardized agenda templates to ensure all meetings have clear objectives and outcomes.",
            "status": "open",
            "priority": "medium",
            "assigned_to": null,
            "due_date": null,
            "created_at": "2024-01-15T10:30:00Z",
            "completed_at": null
        }
    ]
}
```

**Error Responses:**

- `400 Bad Request`: No retrospective items found
- `404 Not Found`: Retrospective not found
- `500 Internal Server Error`: AI service unavailable or error

## Prerequisites

1. **Ollama Installation**: Make sure Ollama is installed and running on your system
2. **Mistral Model**: The Mistral model should be available in Ollama
3. **Retrospective Items**: The retrospective must have at least one item before generating action items

## Setup Instructions

1. Install the required dependency:
   ```bash
   pip install ollama==0.1.7
   ```

2. Start Ollama service:
   ```bash
   ollama serve
   ```

3. Pull the Mistral model (if not already available):
   ```bash
   ollama pull mistral
   ```

## Usage Examples

### Frontend Integration

```javascript
// Generate action items for a retrospective
const generateActionItems = async (retrospectiveId) => {
    try {
        const response = await fetch(`/api/retrospectives/${retrospectiveId}/generate_action_items/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
        });
        
        if (response.ok) {
            const data = await response.json();
            console.log('Generated action items:', data.action_items);
            return data.action_items;
        } else {
            const error = await response.json();
            console.error('Error generating action items:', error.error);
            throw new Error(error.error);
        }
    } catch (error) {
        console.error('Failed to generate action items:', error);
        throw error;
    }
};
```

### cURL Example

```bash
curl -X POST http://localhost:8000/api/retrospectives/1/generate_action_items/ \
     -H "Content-Type: application/json"
```

## How It Works

1. **Data Collection**: The API retrieves all items from the specified retrospective
2. **AI Analysis**: The retrospective items are sent to Ollama with a system prompt designed for agile retrospectives
3. **Response Processing**: The AI response is parsed and validated
4. **Database Storage**: Valid action items are created as `ActionItem` objects in the database
5. **Response**: The created action items are returned to the client

## AI Prompt Engineering

The system uses a carefully crafted prompt that:
- Instructs the AI to act as a team leader for agile retrospectives
- Requests specific, actionable insights
- Limits output to 3-5 most important action items
- Ensures proper JSON formatting
- Focuses on team performance improvement

## Error Handling

The API includes comprehensive error handling for:
- Missing retrospective items
- Invalid retrospective IDs
- AI service unavailability
- Malformed AI responses
- Database errors

## Testing

Run the tests to verify the API functionality:

```bash
python manage.py test api.test_views.TestRetrospectiveViewSet
```

Note: Tests will skip if Ollama is not available, as they require the AI service to be running.

## Future Enhancements

Potential improvements for the future:
- Support for different AI models
- Customizable prompts per team
- Batch processing for multiple retrospectives
- Integration with project management tools
- Action item prioritization based on team preferences
