"""Todo service layer for business logic and data operations."""

import json
import logging
import os
from typing import List, Optional, Dict, Any

from models.todo import TodoModel, validate_todo_data, DEFAULT_PRIORITY, VALID_PRIORITIES

logger = logging.getLogger(__name__)

TODO_FILE = 'todos.json'


class TodoService:
    """Service class for todo operations."""
    
    def __init__(self):
        self.todos: List[TodoModel] = []
        self.next_id = 1
        self.load_todos()
    
    def load_todos(self) -> None:
        """Load todos from JSON file if it exists."""
        if not os.path.exists(TODO_FILE):
            logger.info(f"{TODO_FILE} not found, starting with empty todo list")
            return
        
        try:
            with open(TODO_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                todo_dicts = data.get('todos', [])
                self.todos = [TodoModel.from_dict(todo_dict) for todo_dict in todo_dicts]
                self.next_id = data.get('next_id', 1)
                logger.info(f"Loaded {len(self.todos)} todos from {TODO_FILE}")
        except (json.JSONDecodeError, IOError) as e:
            logger.error(f"Error loading todos: {e}")
            self.todos = []
            self.next_id = 1
    
    def save_todos(self) -> None:
        """Save todos to JSON file."""
        try:
            data = {
                'todos': [todo.to_dict() for todo in self.todos],
                'next_id': self.next_id
            }
            with open(TODO_FILE, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
            logger.info(f"Saved {len(self.todos)} todos to {TODO_FILE}")
        except IOError as e:
            logger.error(f"Error saving todos: {e}")
            raise
    
    def get_all_todos(self) -> List[Dict]:
        """Get all todos as dictionaries."""
        return [todo.to_dict() for todo in self.todos]
    
    def get_all_todo_objects(self) -> List[TodoModel]:
        """Get all todos as TodoModel objects."""
        return self.todos
    
    def find_todo_by_id(self, todo_id: int) -> Optional[TodoModel]:
        """Find todo by ID."""
        return next((todo for todo in self.todos if todo.id == todo_id), None)
    
    def create_todo(self, title: str, description: str = '', priority: str = DEFAULT_PRIORITY) -> TodoModel:
        """Create a new todo."""
        todo = TodoModel(self.next_id, title, description, priority)
        self.todos.append(todo)
        self.next_id += 1
        self.save_todos()
        logger.info(f"Created todo: {todo.title}")
        return todo
    
    def update_todo(self, todo_id: int, data: Dict[str, Any]) -> Optional[TodoModel]:
        """Update an existing todo."""
        todo = self.find_todo_by_id(todo_id)
        if not todo:
            return None
        
        if 'title' in data:
            todo.title = data['title'].strip()
        if 'description' in data:
            todo.description = data['description'].strip()
        if 'completed' in data:
            todo.completed = bool(data['completed'])
        if 'priority' in data:
            todo.priority = data['priority']
        
        self.save_todos()
        logger.info(f"Updated todo {todo_id}: {todo.title}")
        return todo
    
    def delete_todo(self, todo_id: int) -> bool:
        """Delete a todo by ID. Returns True if deleted, False if not found."""
        initial_count = len(self.todos)
        self.todos = [todo for todo in self.todos if todo.id != todo_id]
        
        if len(self.todos) < initial_count:
            self.save_todos()
            logger.info(f"Deleted todo {todo_id}")
            return True
        return False
    
    def toggle_todo_completion(self, todo_id: int) -> Optional[TodoModel]:
        """Toggle todo completion status."""
        todo = self.find_todo_by_id(todo_id)
        if todo:
            todo.completed = not todo.completed
            self.save_todos()
            logger.info(f"Toggled todo {todo_id}: {todo.title}")
        return todo
    
    def validate_form_data(self, title: str, priority: str) -> tuple[str, str]:
        """Validate and clean form data."""
        title = title.strip() if title else ''
        
        # Validate priority
        if priority not in VALID_PRIORITIES:
            priority = DEFAULT_PRIORITY
        
        return title, priority


# Global service instance
todo_service = TodoService()
