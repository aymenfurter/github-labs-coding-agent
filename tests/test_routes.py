"""Unit tests for todo routes."""

import pytest
import json
from unittest.mock import patch, MagicMock
from models.todo import TodoModel


class TestTodoRoutes:
    """Test cases for todo routes."""
    
    def test_index_route(self, client):
        """Test the main index route."""
        with patch('routes.todo_routes.todo_service') as mock_service:
            mock_todo = TodoModel(1, "Test Todo", "Test description", "medium", False)
            mock_service.get_all_todo_objects.return_value = [mock_todo]
            
            response = client.get('/')
            
            assert response.status_code == 200
            mock_service.get_all_todo_objects.assert_called_once()
    
    def test_get_todos_api(self, client):
        """Test the GET /api/todos endpoint."""
        with patch('routes.todo_routes.todo_service') as mock_service:
            test_todos = [
                {'id': 1, 'title': 'Todo 1', 'completed': False},
                {'id': 2, 'title': 'Todo 2', 'completed': True}
            ]
            mock_service.get_all_todos.return_value = test_todos
            
            response = client.get('/api/todos')
            
            assert response.status_code == 200
            assert response.get_json() == test_todos
            mock_service.get_all_todos.assert_called_once()
    
    def test_create_todo_api_success(self, client):
        """Test successful todo creation via API."""
        with patch('routes.todo_routes.todo_service') as mock_service:
            mock_todo = TodoModel(1, "New Todo", "Description", "high")
            mock_service.create_todo.return_value = mock_todo
            
            data = {
                'title': 'New Todo',
                'description': 'Description',
                'priority': 'high'
            }
            
            response = client.post('/api/todos', json=data)
            
            assert response.status_code == 201
            result = response.get_json()
            assert result['title'] == 'New Todo'
            assert result['description'] == 'Description'
            assert result['priority'] == 'high'
            
            mock_service.create_todo.assert_called_once_with('New Todo', 'Description', 'high')
    
    def test_create_todo_api_validation_error(self, client):
        """Test todo creation with validation errors."""
        data = {
            'title': '',  # Empty title should cause validation error
            'priority': 'invalid_priority'
        }
        
        response = client.post('/api/todos', json=data)
        
        assert response.status_code == 400
        result = response.get_json()
        assert 'errors' in result
        assert len(result['errors']) > 0
    
    def test_create_todo_api_exception(self, client):
        """Test todo creation when service raises exception."""
        with patch('routes.todo_routes.todo_service') as mock_service:
            mock_service.create_todo.side_effect = Exception("Database error")
            
            data = {'title': 'New Todo'}
            
            response = client.post('/api/todos', json=data)
            
            assert response.status_code == 500
            result = response.get_json()
            assert result['error'] == 'Internal server error'
    
    def test_update_todo_api_success(self, client):
        """Test successful todo update via API."""
        with patch('routes.todo_routes.todo_service') as mock_service:
            mock_todo = TodoModel(1, "Updated Todo", "Updated Description", "high")
            mock_service.update_todo.return_value = mock_todo
            
            data = {
                'title': 'Updated Todo',
                'description': 'Updated Description',
                'completed': True
            }
            
            response = client.put('/api/todos/1', json=data)
            
            assert response.status_code == 200
            result = response.get_json()
            assert result['title'] == 'Updated Todo'
            assert result['description'] == 'Updated Description'
            
            mock_service.update_todo.assert_called_once_with(1, data)
    
    def test_update_todo_api_not_found(self, client):
        """Test updating non-existent todo."""
        with patch('routes.todo_routes.todo_service') as mock_service:
            mock_service.update_todo.return_value = None
            
            data = {'title': 'Updated Todo'}
            
            response = client.put('/api/todos/999', json=data)
            
            assert response.status_code == 404
            result = response.get_json()
            assert result['error'] == 'Todo not found'
    
    def test_update_todo_api_validation_error(self, client):
        """Test todo update with validation errors."""
        data = {
            'title': 'x' * 201,  # Title too long
            'priority': 'invalid_priority'
        }
        
        response = client.put('/api/todos/1', json=data)
        
        assert response.status_code == 400
        result = response.get_json()
        assert 'errors' in result
    
    def test_delete_todo_api_success(self, client):
        """Test successful todo deletion via API."""
        with patch('routes.todo_routes.todo_service') as mock_service:
            mock_service.delete_todo.return_value = True
            
            response = client.delete('/api/todos/1')
            
            assert response.status_code == 200
            result = response.get_json()
            assert result['message'] == 'Todo deleted successfully'
            
            mock_service.delete_todo.assert_called_once_with(1)
    
    def test_delete_todo_api_not_found(self, client):
        """Test deleting non-existent todo."""
        with patch('routes.todo_routes.todo_service') as mock_service:
            mock_service.delete_todo.return_value = False
            
            response = client.delete('/api/todos/999')
            
            assert response.status_code == 404
            result = response.get_json()
            assert result['error'] == 'Todo not found'
    
    def test_delete_todo_api_exception(self, client):
        """Test todo deletion when service raises exception."""
        with patch('routes.todo_routes.todo_service') as mock_service:
            mock_service.delete_todo.side_effect = Exception("Database error")
            
            response = client.delete('/api/todos/1')
            
            assert response.status_code == 500
            result = response.get_json()
            assert result['error'] == 'Internal server error'
    
    def test_add_todo_form_success(self, client):
        """Test successful todo creation via form."""
        with patch('routes.todo_routes.todo_service') as mock_service:
            mock_service.validate_form_data.return_value = ("Valid Title", "medium")
            mock_service.create_todo.return_value = TodoModel(1, "Valid Title")
            
            data = {
                'title': 'Valid Title',
                'description': 'Description',
                'priority': 'medium'
            }
            
            response = client.post('/add', data=data)
            
            assert response.status_code == 302  # Redirect
            assert response.location.endswith('/')
            
            mock_service.validate_form_data.assert_called_once_with('Valid Title', 'medium')
            mock_service.create_todo.assert_called_once_with('Valid Title', 'Description', 'medium')
    
    def test_add_todo_form_empty_title(self, client):
        """Test form submission with empty title."""
        with patch('routes.todo_routes.todo_service') as mock_service:
            mock_service.validate_form_data.return_value = ("", "medium")
            
            data = {'title': '', 'description': 'Description'}
            
            response = client.post('/add', data=data)
            
            assert response.status_code == 302  # Redirect
            mock_service.create_todo.assert_not_called()
    
    def test_add_todo_form_exception(self, client):
        """Test form submission when service raises exception."""
        with patch('routes.todo_routes.todo_service') as mock_service:
            mock_service.validate_form_data.return_value = ("Valid Title", "medium")
            mock_service.create_todo.side_effect = Exception("Database error")
            
            data = {'title': 'Valid Title'}
            
            response = client.post('/add', data=data)
            
            assert response.status_code == 302  # Should still redirect even on error
    
    def test_toggle_todo_success(self, client):
        """Test successful todo toggle."""
        with patch('routes.todo_routes.todo_service') as mock_service:
            mock_service.toggle_todo_completion.return_value = TodoModel(1, "Test")
            
            response = client.get('/toggle/1')
            
            assert response.status_code == 302  # Redirect
            assert response.location.endswith('/')
            
            mock_service.toggle_todo_completion.assert_called_once_with(1)
    
    def test_toggle_todo_exception(self, client):
        """Test todo toggle when service raises exception."""
        with patch('routes.todo_routes.todo_service') as mock_service:
            mock_service.toggle_todo_completion.side_effect = Exception("Database error")
            
            response = client.get('/toggle/1')
            
            assert response.status_code == 302  # Should still redirect even on error
    
    def test_delete_todo_form_success(self, client):
        """Test successful todo deletion via form."""
        with patch('routes.todo_routes.todo_service') as mock_service:
            mock_service.delete_todo.return_value = True
            
            response = client.get('/delete/1')
            
            assert response.status_code == 302  # Redirect
            assert response.location.endswith('/')
            
            mock_service.delete_todo.assert_called_once_with(1)
    
    def test_delete_todo_form_exception(self, client):
        """Test todo deletion via form when service raises exception."""
        with patch('routes.todo_routes.todo_service') as mock_service:
            mock_service.delete_todo.side_effect = Exception("Database error")
            
            response = client.get('/delete/1')
            
            assert response.status_code == 302  # Should still redirect even on error


class TestAppErrorHandlers:
    """Test cases for application error handlers."""
    
    def test_404_error_handler(self, client):
        """Test 404 error handler."""
        response = client.get('/nonexistent-route')
        
        assert response.status_code == 404
        result = response.get_json()
        assert result['error'] == 'Not found'