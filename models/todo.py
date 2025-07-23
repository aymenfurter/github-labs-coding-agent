"""Todo model and validation logic."""

from datetime import datetime
from typing import Dict, List, Optional

# Constants
DEFAULT_PRIORITY = 'medium'
VALID_PRIORITIES = {'low', 'medium', 'high'}
MAX_TITLE_LENGTH = 200
MAX_DESCRIPTION_LENGTH = 1000


class TodoModel:
    """Todo data model with validation."""
    
    def __init__(self, todo_id: int, title: str, description: str = '', 
                 priority: str = DEFAULT_PRIORITY, completed: bool = False,
                 created_at: str = None):
        self.id = todo_id
        self.title = title.strip()
        self.description = description.strip()
        self.priority = priority
        self.completed = completed
        self.created_at = created_at or datetime.now().isoformat()
    
    def to_dict(self) -> Dict:
        """Convert todo to dictionary."""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'completed': self.completed,
            'created_at': self.created_at,
            'priority': self.priority
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'TodoModel':
        """Create todo from dictionary."""
        return cls(
            todo_id=data['id'],
            title=data['title'],
            description=data.get('description', ''),
            priority=data.get('priority', DEFAULT_PRIORITY),
            completed=data.get('completed', False),
            created_at=data.get('created_at')
        )


def validate_todo_data(data: Dict, is_update: bool = False) -> List[str]:
    """Validate todo data and return list of errors."""
    errors = []
    
    # Check if title is required and present
    if not is_update:
        if not data or 'title' not in data or not data.get('title', '').strip():
            errors.append('Title is required')
    
    title = data.get('title', '').strip()
    if title and len(title) > MAX_TITLE_LENGTH:
        errors.append(f'Title must be {MAX_TITLE_LENGTH} characters or less')
    
    description = data.get('description', '').strip()
    if description and len(description) > MAX_DESCRIPTION_LENGTH:
        errors.append(f'Description must be {MAX_DESCRIPTION_LENGTH} characters or less')
    
    priority = data.get('priority', DEFAULT_PRIORITY)
    if priority not in VALID_PRIORITIES:
        errors.append(f'Priority must be one of: {", ".join(VALID_PRIORITIES)}')
    
    return errors
