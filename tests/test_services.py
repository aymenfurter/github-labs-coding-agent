"""Unit tests for TodoService class."""

import pytest
import json
import os
from unittest.mock import patch, mock_open
from services.todo_service import TodoService
from models.todo import TodoModel, DEFAULT_PRIORITY


class TestTodoService:
    """Test cases for TodoService class."""
    
    def test_todo_service_init_empty(self, temp_todo_file):
        """Test TodoService initialization with no existing file."""
        with patch('services.todo_service.TODO_FILE', temp_todo_file):
            service = TodoService()
            assert service.todos == []
            assert service.next_id == 1
    
    def test_todo_service_init_with_data(self, temp_todo_file):
        """Test TodoService initialization with existing data."""
        # Setup test data
        test_data = {
            'todos': [
                {
                    'id': 1,
                    'title': 'Test Todo',
                    'description': 'Test Description',
                    'priority': 'high',
                    'completed': False,
                    'created_at': '2023-01-01T12:00:00'
                }
            ],
            'next_id': 2
        }
        
        with open(temp_todo_file, 'w') as f:
            json.dump(test_data, f)
        
        with patch('services.todo_service.TODO_FILE', temp_todo_file):
            service = TodoService()
            assert len(service.todos) == 1
            assert service.next_id == 2
            assert service.todos[0].title == 'Test Todo'
    
    def test_todo_service_load_todos_invalid_json(self, temp_todo_file):
        """Test TodoService handles invalid JSON gracefully."""
        with open(temp_todo_file, 'w') as f:
            f.write("invalid json content")
        
        with patch('services.todo_service.TODO_FILE', temp_todo_file):
            service = TodoService()
            assert service.todos == []
            assert service.next_id == 1
    
    def test_get_all_todos(self):
        """Test getting all todos as dictionaries."""
        service = TodoService()
        service.todos = [
            TodoModel(1, "Todo 1"),
            TodoModel(2, "Todo 2")
        ]
        
        todos = service.get_all_todos()
        assert len(todos) == 2
        assert todos[0]['title'] == "Todo 1"
        assert todos[1]['title'] == "Todo 2"
    
    def test_get_all_todo_objects(self):
        """Test getting all todos as TodoModel objects."""
        service = TodoService()
        todo1 = TodoModel(1, "Todo 1")
        todo2 = TodoModel(2, "Todo 2")
        service.todos = [todo1, todo2]
        
        todos = service.get_all_todo_objects()
        assert len(todos) == 2
        assert todos[0] == todo1
        assert todos[1] == todo2
    
    def test_find_todo_by_id(self):
        """Test finding todo by ID."""
        service = TodoService()
        todo1 = TodoModel(1, "Todo 1")
        todo2 = TodoModel(2, "Todo 2")
        service.todos = [todo1, todo2]
        
        found_todo = service.find_todo_by_id(1)
        assert found_todo == todo1
        
        found_todo = service.find_todo_by_id(2)
        assert found_todo == todo2
        
        found_todo = service.find_todo_by_id(999)
        assert found_todo is None
    
    @patch('services.todo_service.TodoService.save_todos')
    def test_create_todo(self, mock_save):
        """Test creating a new todo."""
        service = TodoService()
        service.next_id = 5
        
        todo = service.create_todo("New Todo", "Description", "high")
        
        assert todo.id == 5
        assert todo.title == "New Todo"
        assert todo.description == "Description"
        assert todo.priority == "high"
        assert todo.completed is False
        assert service.next_id == 6
        assert todo in service.todos
        mock_save.assert_called_once()
    
    @patch('services.todo_service.TodoService.save_todos')
    def test_create_todo_defaults(self, mock_save):
        """Test creating todo with default values."""
        service = TodoService()
        
        todo = service.create_todo("New Todo")
        
        assert todo.title == "New Todo"
        assert todo.description == ""
        assert todo.priority == DEFAULT_PRIORITY
    
    @patch('services.todo_service.TodoService.save_todos')
    def test_update_todo(self, mock_save):
        """Test updating an existing todo."""
        service = TodoService()
        original_todo = TodoModel(1, "Original", "Original desc", "low")
        service.todos = [original_todo]
        
        update_data = {
            'title': 'Updated Title',
            'description': 'Updated Description',
            'priority': 'high',
            'completed': True
        }
        
        updated_todo = service.update_todo(1, update_data)
        
        assert updated_todo == original_todo
        assert updated_todo.title == 'Updated Title'
        assert updated_todo.description == 'Updated Description'
        assert updated_todo.priority == 'high'
        assert updated_todo.completed is True
        mock_save.assert_called_once()
    
    @patch('services.todo_service.TodoService.save_todos')
    def test_update_todo_partial(self, mock_save):
        """Test updating todo with partial data."""
        service = TodoService()
        original_todo = TodoModel(1, "Original", "Original desc", "low")
        service.todos = [original_todo]
        
        update_data = {'title': 'Updated Title Only'}
        
        updated_todo = service.update_todo(1, update_data)
        
        assert updated_todo.title == 'Updated Title Only'
        assert updated_todo.description == 'Original desc'  # Unchanged
        assert updated_todo.priority == 'low'  # Unchanged
        assert updated_todo.completed is False  # Unchanged
        mock_save.assert_called_once()
    
    def test_update_todo_not_found(self):
        """Test updating non-existent todo."""
        service = TodoService()
        service.todos = []
        
        result = service.update_todo(999, {'title': 'New Title'})
        assert result is None
    
    @patch('services.todo_service.TodoService.save_todos')
    def test_delete_todo(self, mock_save):
        """Test deleting an existing todo."""
        service = TodoService()
        todo1 = TodoModel(1, "Todo 1")
        todo2 = TodoModel(2, "Todo 2")
        service.todos = [todo1, todo2]
        
        result = service.delete_todo(1)
        
        assert result is True
        assert len(service.todos) == 1
        assert service.todos[0] == todo2
        mock_save.assert_called_once()
    
    def test_delete_todo_not_found(self):
        """Test deleting non-existent todo."""
        service = TodoService()
        todo1 = TodoModel(1, "Todo 1")
        service.todos = [todo1]
        
        result = service.delete_todo(999)
        
        assert result is False
        assert len(service.todos) == 1  # Unchanged
    
    @patch('services.todo_service.TodoService.save_todos')
    def test_toggle_todo_completion(self, mock_save):
        """Test toggling todo completion status."""
        service = TodoService()
        todo = TodoModel(1, "Todo", completed=False)
        service.todos = [todo]
        
        result = service.toggle_todo_completion(1)
        
        assert result == todo
        assert todo.completed is True
        mock_save.assert_called_once()
        
        # Toggle again
        mock_save.reset_mock()
        result = service.toggle_todo_completion(1)
        
        assert result == todo
        assert todo.completed is False
        mock_save.assert_called_once()
    
    def test_toggle_todo_completion_not_found(self):
        """Test toggling completion for non-existent todo."""
        service = TodoService()
        service.todos = []
        
        result = service.toggle_todo_completion(999)
        assert result is None
    
    def test_validate_form_data(self):
        """Test form data validation and cleaning."""
        service = TodoService()
        
        # Test normal case
        title, priority = service.validate_form_data("  Test Title  ", "high")
        assert title == "Test Title"
        assert priority == "high"
        
        # Test invalid priority
        title, priority = service.validate_form_data("Test Title", "invalid")
        assert title == "Test Title"
        assert priority == DEFAULT_PRIORITY
        
        # Test empty title
        title, priority = service.validate_form_data("", "low")
        assert title == ""
        assert priority == "low"
        
        # Test None title
        title, priority = service.validate_form_data(None, "medium")
        assert title == ""
        assert priority == "medium"
    
    def test_save_todos(self, temp_todo_file):
        """Test saving todos to file."""
        service = TodoService()
        service.todos = [
            TodoModel(1, "Todo 1", "Description 1", "high"),
            TodoModel(2, "Todo 2", "Description 2", "low")
        ]
        service.next_id = 3
        
        with patch('services.todo_service.TODO_FILE', temp_todo_file):
            service.save_todos()
        
        # Verify file contents
        with open(temp_todo_file, 'r') as f:
            data = json.load(f)
        
        assert len(data['todos']) == 2
        assert data['next_id'] == 3
        assert data['todos'][0]['title'] == "Todo 1"
        assert data['todos'][1]['title'] == "Todo 2"
    
    def test_save_todos_io_error(self):
        """Test save_todos handles IO errors."""
        service = TodoService()
        
        with patch('builtins.open', mock_open()) as mock_file:
            mock_file.side_effect = IOError("Permission denied")
            
            with pytest.raises(IOError):
                service.save_todos()