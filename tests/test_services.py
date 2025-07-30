"""Unit tests for todo services."""

import os
import json
import tempfile
import pytest
from unittest.mock import patch, mock_open, MagicMock

from models.todo import TodoModel
from services.todo_service import TodoService, todo_service


class TestTodoService:
    """Test TodoService class."""
    
    def test_init(self):
        """Test TodoService initialization."""
        with patch('services.todo_service.os.path.exists', return_value=False):
            service = TodoService()
            assert service.todos == []
            assert service.next_id == 1
    
    def test_get_all_todos_empty(self, clean_todo_service):
        """Test getting all todos when empty."""
        result = clean_todo_service.get_all_todos()
        assert result == []
    
    def test_get_all_todos_with_data(self, clean_todo_service):
        """Test getting all todos with data."""
        # Add some todos manually
        todo1 = TodoModel(1, "Todo 1")
        todo2 = TodoModel(2, "Todo 2")
        clean_todo_service.todos = [todo1, todo2]
        
        result = clean_todo_service.get_all_todos()
        assert len(result) == 2
        assert all(isinstance(item, dict) for item in result)
        assert result[0]['title'] == "Todo 1"
        assert result[1]['title'] == "Todo 2"
    
    def test_find_todo_by_id_exists(self, clean_todo_service):
        """Test finding todo by ID when it exists."""
        todo = TodoModel(5, "Find me")
        clean_todo_service.todos = [todo]
        
        result = clean_todo_service.find_todo_by_id(5)
        assert result is not None
        assert result.id == 5
        assert result.title == "Find me"
    
    def test_find_todo_by_id_not_exists(self, clean_todo_service):
        """Test finding todo by ID when it doesn't exist."""
        result = clean_todo_service.find_todo_by_id(999)
        assert result is None
    
    def test_create_todo_basic(self, clean_todo_service):
        """Test creating a basic todo."""
        with patch.object(clean_todo_service, 'save_todos'):
            todo = clean_todo_service.create_todo("New Todo")
            
            assert todo.id == 1
            assert todo.title == "New Todo"
            assert todo.description == ""
            assert todo.priority == "medium"
            assert not todo.completed
            assert len(clean_todo_service.todos) == 1
            assert clean_todo_service.next_id == 2
    
    def test_create_todo_with_details(self, clean_todo_service):
        """Test creating a todo with all details."""
        with patch.object(clean_todo_service, 'save_todos'):
            todo = clean_todo_service.create_todo(
                "Detailed Todo",
                "This is a description",
                "high"
            )
            
            assert todo.title == "Detailed Todo"
            assert todo.description == "This is a description"
            assert todo.priority == "high"
    
    def test_create_todo_increments_id(self, clean_todo_service):
        """Test that creating todos increments the ID."""
        with patch.object(clean_todo_service, 'save_todos'):
            todo1 = clean_todo_service.create_todo("Todo 1")
            todo2 = clean_todo_service.create_todo("Todo 2")
            
            assert todo1.id == 1
            assert todo2.id == 2
            assert clean_todo_service.next_id == 3
    
    def test_update_todo_exists(self, clean_todo_service):
        """Test updating an existing todo."""
        todo = TodoModel(1, "Original Title")
        clean_todo_service.todos = [todo]
        
        update_data = {
            'title': 'Updated Title',
            'description': 'New description',
            'completed': True,
            'priority': 'high'
        }
        
        with patch.object(clean_todo_service, 'save_todos'):
            result = clean_todo_service.update_todo(1, update_data)
            
            assert result is not None
            assert result.title == 'Updated Title'
            assert result.description == 'New description'
            assert result.completed is True
            assert result.priority == 'high'
    
    def test_update_todo_partial(self, clean_todo_service):
        """Test partially updating a todo."""
        todo = TodoModel(1, "Original Title", "Original description")
        clean_todo_service.todos = [todo]
        
        update_data = {'title': 'Updated Title'}
        
        with patch.object(clean_todo_service, 'save_todos'):
            result = clean_todo_service.update_todo(1, update_data)
            
            assert result.title == 'Updated Title'
            assert result.description == 'Original description'  # Should remain unchanged
    
    def test_update_todo_not_exists(self, clean_todo_service):
        """Test updating a non-existent todo."""
        result = clean_todo_service.update_todo(999, {'title': 'New Title'})
        assert result is None
    
    def test_delete_todo_exists(self, clean_todo_service):
        """Test deleting an existing todo."""
        todo1 = TodoModel(1, "Todo 1")
        todo2 = TodoModel(2, "Todo 2")
        clean_todo_service.todos = [todo1, todo2]
        
        with patch.object(clean_todo_service, 'save_todos'):
            result = clean_todo_service.delete_todo(1)
            
            assert result is True
            assert len(clean_todo_service.todos) == 1
            assert clean_todo_service.todos[0].id == 2
    
    def test_delete_todo_not_exists(self, clean_todo_service):
        """Test deleting a non-existent todo."""
        todo = TodoModel(1, "Todo 1")
        clean_todo_service.todos = [todo]
        
        result = clean_todo_service.delete_todo(999)
        assert result is False
        assert len(clean_todo_service.todos) == 1  # No change
    
    def test_toggle_todo_completion_exists(self, clean_todo_service):
        """Test toggling completion status of existing todo."""
        todo = TodoModel(1, "Todo 1", completed=False)
        clean_todo_service.todos = [todo]
        
        with patch.object(clean_todo_service, 'save_todos'):
            result = clean_todo_service.toggle_todo_completion(1)
            
            assert result is not None
            assert result.completed is True
            
            # Toggle again
            result = clean_todo_service.toggle_todo_completion(1)
            assert result.completed is False
    
    def test_toggle_todo_completion_not_exists(self, clean_todo_service):
        """Test toggling completion status of non-existent todo."""
        result = clean_todo_service.toggle_todo_completion(999)
        assert result is None
    
    def test_validate_form_data_valid(self, clean_todo_service):
        """Test validating valid form data."""
        title, priority = clean_todo_service.validate_form_data("Test Title", "high")
        assert title == "Test Title"
        assert priority == "high"
    
    def test_validate_form_data_strips_title(self, clean_todo_service):
        """Test form data validation strips title."""
        title, priority = clean_todo_service.validate_form_data("  Test Title  ", "medium")
        assert title == "Test Title"
    
    def test_validate_form_data_empty_title(self, clean_todo_service):
        """Test form data validation with empty title."""
        title, priority = clean_todo_service.validate_form_data("", "medium")
        assert title == ""
    
    def test_validate_form_data_none_title(self, clean_todo_service):
        """Test form data validation with None title."""
        title, priority = clean_todo_service.validate_form_data(None, "medium")
        assert title == ""
    
    def test_validate_form_data_invalid_priority(self, clean_todo_service):
        """Test form data validation with invalid priority."""
        title, priority = clean_todo_service.validate_form_data("Test Title", "invalid")
        assert title == "Test Title"
        assert priority == "medium"  # Should default to medium
    
    def test_validate_form_data_valid_priorities(self, clean_todo_service):
        """Test form data validation with all valid priorities."""
        for valid_priority in ['low', 'medium', 'high']:
            title, priority = clean_todo_service.validate_form_data("Test", valid_priority)
            assert priority == valid_priority


class TestTodoServicePersistence:
    """Test TodoService persistence methods."""
    
    def test_load_todos_no_file(self, clean_todo_service):
        """Test loading todos when file doesn't exist."""
        with patch('os.path.exists', return_value=False):
            clean_todo_service.load_todos()
            
            assert clean_todo_service.todos == []
            assert clean_todo_service.next_id == 1
    
    def test_load_todos_valid_file(self, clean_todo_service):
        """Test loading todos from valid file."""
        mock_data = {
            'todos': [
                {'id': 1, 'title': 'Todo 1', 'completed': False, 'priority': 'medium'},
                {'id': 2, 'title': 'Todo 2', 'completed': True, 'priority': 'high'}
            ],
            'next_id': 3
        }
        
        with patch('os.path.exists', return_value=True), \
             patch('builtins.open', mock_open(read_data=json.dumps(mock_data))):
            
            clean_todo_service.load_todos()
            
            assert len(clean_todo_service.todos) == 2
            assert clean_todo_service.next_id == 3
            assert clean_todo_service.todos[0].title == 'Todo 1'
            assert clean_todo_service.todos[1].title == 'Todo 2'
    
    def test_load_todos_invalid_json(self, clean_todo_service):
        """Test loading todos with invalid JSON."""
        with patch('os.path.exists', return_value=True), \
             patch('builtins.open', mock_open(read_data='invalid json')):
            
            clean_todo_service.load_todos()
            
            assert clean_todo_service.todos == []
            assert clean_todo_service.next_id == 1
    
    def test_load_todos_io_error(self, clean_todo_service):
        """Test loading todos with IO error."""
        with patch('os.path.exists', return_value=True), \
             patch('builtins.open', side_effect=IOError("File error")):
            
            clean_todo_service.load_todos()
            
            assert clean_todo_service.todos == []
            assert clean_todo_service.next_id == 1
    
    def test_save_todos_success(self, clean_todo_service):
        """Test saving todos successfully."""
        todo = TodoModel(1, "Test Todo")
        clean_todo_service.todos = [todo]
        clean_todo_service.next_id = 2
        
        mock_file = mock_open()
        with patch('builtins.open', mock_file):
            clean_todo_service.save_todos()
            
            # Check that file was opened for writing
            mock_file.assert_called_once_with('todos.json', 'w', encoding='utf-8')
            
            # Check that json.dump was called (indirectly via the write calls)
            handle = mock_file()
            written_content = ''.join(call.args[0] for call in handle.write.call_args_list)
            assert 'Test Todo' in written_content
    
    def test_save_todos_io_error(self, clean_todo_service):
        """Test saving todos with IO error."""
        with patch('builtins.open', side_effect=IOError("Write error")):
            with pytest.raises(IOError):
                clean_todo_service.save_todos()


class TestGlobalServiceInstance:
    """Test the global todo_service instance."""
    
    def test_global_service_exists(self):
        """Test that global service instance exists."""
        assert todo_service is not None
        assert isinstance(todo_service, TodoService)
    
    def test_global_service_has_methods(self):
        """Test that global service has required methods."""
        methods = [
            'load_todos', 'save_todos', 'get_all_todos', 'find_todo_by_id',
            'create_todo', 'update_todo', 'delete_todo', 'toggle_todo_completion',
            'validate_form_data'
        ]
        
        for method in methods:
            assert hasattr(todo_service, method)
            assert callable(getattr(todo_service, method))