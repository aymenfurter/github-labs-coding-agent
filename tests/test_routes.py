"""Unit tests for todo routes."""

import json
import pytest
from unittest.mock import patch, MagicMock

from models.todo import TodoModel


class TestTodoRoutes:
    """Test todo route handlers."""
    
    def test_index_route(self, client):
        """Test the index route."""
        with patch('services.todo_service.todo_service.get_all_todos', return_value=[]):
            response = client.get('/')
            assert response.status_code == 200
    
    def test_get_todos_api_empty(self, client):
        """Test GET /api/todos with empty list."""
        with patch('services.todo_service.todo_service.get_all_todos', return_value=[]):
            response = client.get('/api/todos')
            assert response.status_code == 200
            assert response.get_json() == []
    
    def test_get_todos_api_with_data(self, client):
        """Test GET /api/todos with data."""
        mock_todos = [
            {'id': 1, 'title': 'Todo 1', 'completed': False},
            {'id': 2, 'title': 'Todo 2', 'completed': True}
        ]
        
        with patch('services.todo_service.todo_service.get_all_todos', return_value=mock_todos):
            response = client.get('/api/todos')
            assert response.status_code == 200
            assert response.get_json() == mock_todos
    
    def test_create_todo_api_valid(self, client):
        """Test POST /api/todos with valid data."""
        mock_todo = TodoModel(1, "New Todo", "Description", "high")
        
        with patch('models.todo.validate_todo_data', return_value=[]), \
             patch('services.todo_service.todo_service.create_todo', return_value=mock_todo):
            
            response = client.post('/api/todos', 
                                 json={'title': 'New Todo', 'description': 'Description', 'priority': 'high'})
            
            assert response.status_code == 201
            data = response.get_json()
            assert data['title'] == 'New Todo'
            assert data['description'] == 'Description'
            assert data['priority'] == 'high'
    
    def test_create_todo_api_validation_errors(self, client):
        """Test POST /api/todos with validation errors."""
        with patch('models.todo.validate_todo_data', return_value=['Title is required']):
            response = client.post('/api/todos', json={})
            
            assert response.status_code == 400
            data = response.get_json()
            assert 'errors' in data
            assert 'Title is required' in data['errors']
    
    def test_create_todo_api_server_error(self, client):
        """Test POST /api/todos with server error."""
        with patch('models.todo.validate_todo_data', return_value=[]), \
             patch('services.todo_service.todo_service.create_todo', side_effect=Exception("Server error")):
            
            response = client.post('/api/todos', json={'title': 'Test'})
            
            assert response.status_code == 500
            data = response.get_json()
            assert data['error'] == 'Internal server error'
    
    def test_update_todo_api_valid(self, client):
        """Test PUT /api/todos/<id> with valid data."""
        mock_todo = TodoModel(1, "Updated Todo", "Updated description", "low", True)
        
        with patch('models.todo.validate_todo_data', return_value=[]), \
             patch('services.todo_service.todo_service.update_todo', return_value=mock_todo):
            
            response = client.put('/api/todos/1', 
                                json={'title': 'Updated Todo', 'completed': True})
            
            assert response.status_code == 200
            data = response.get_json()
            assert data['title'] == 'Updated Todo'
            assert data['completed'] is True
    
    def test_update_todo_api_not_found(self, client):
        """Test PUT /api/todos/<id> with non-existent todo."""
        with patch('models.todo.validate_todo_data', return_value=[]), \
             patch('services.todo_service.todo_service.update_todo', return_value=None):
            
            response = client.put('/api/todos/999', json={'title': 'Updated'})
            
            assert response.status_code == 404
            data = response.get_json()
            assert data['error'] == 'Todo not found'
    
    def test_update_todo_api_validation_errors(self, client):
        """Test PUT /api/todos/<id> with validation errors."""
        with patch('models.todo.validate_todo_data', return_value=['Title must be 200 characters or less']):
            response = client.put('/api/todos/1', json={'title': 'x' * 300})
            
            assert response.status_code == 400
            data = response.get_json()
            assert 'errors' in data
            assert 'Title must be 200 characters or less' in data['errors']
    
    def test_update_todo_api_server_error(self, client):
        """Test PUT /api/todos/<id> with server error."""
        with patch('models.todo.validate_todo_data', return_value=[]), \
             patch('services.todo_service.todo_service.update_todo', side_effect=Exception("Server error")):
            
            response = client.put('/api/todos/1', json={'title': 'Test'})
            
            assert response.status_code == 500
            data = response.get_json()
            assert data['error'] == 'Internal server error'
    
    def test_delete_todo_api_success(self, client):
        """Test DELETE /api/todos/<id> successfully."""
        with patch('services.todo_service.todo_service.delete_todo', return_value=True):
            response = client.delete('/api/todos/1')
            
            assert response.status_code == 200
            data = response.get_json()
            assert data['message'] == 'Todo deleted successfully'
    
    def test_delete_todo_api_not_found(self, client):
        """Test DELETE /api/todos/<id> with non-existent todo."""
        with patch('services.todo_service.todo_service.delete_todo', return_value=False):
            response = client.delete('/api/todos/999')
            
            assert response.status_code == 404
            data = response.get_json()
            assert data['error'] == 'Todo not found'
    
    def test_delete_todo_api_server_error(self, client):
        """Test DELETE /api/todos/<id> with server error."""
        with patch('services.todo_service.todo_service.delete_todo', side_effect=Exception("Server error")):
            response = client.delete('/api/todos/1')
            
            assert response.status_code == 500
            data = response.get_json()
            assert data['error'] == 'Internal server error'


class TestTodoFormRoutes:
    """Test todo form route handlers."""
    
    def test_add_todo_form_valid(self, client):
        """Test POST /add with valid form data."""
        mock_todo = TodoModel(1, "Form Todo", "Form description", "medium")
        
        with patch('services.todo_service.todo_service.validate_form_data', return_value=("Form Todo", "medium")), \
             patch('services.todo_service.todo_service.create_todo', return_value=mock_todo):
            
            response = client.post('/add', data={
                'title': 'Form Todo',
                'description': 'Form description',
                'priority': 'medium'
            }, follow_redirects=False)
            
            assert response.status_code == 302  # Redirect after successful creation
            assert response.location.endswith('/')
    
    def test_add_todo_form_empty_title(self, client):
        """Test POST /add with empty title."""
        with patch('services.todo_service.todo_service.validate_form_data', return_value=("", "medium")):
            response = client.post('/add', data={
                'title': '',
                'description': 'Test description',
                'priority': 'medium'
            }, follow_redirects=False)
            
            assert response.status_code == 302  # Still redirects
            assert response.location.endswith('/')
    
    def test_add_todo_form_server_error(self, client):
        """Test POST /add with server error."""
        with patch('services.todo_service.todo_service.validate_form_data', side_effect=Exception("Server error")):
            response = client.post('/add', data={
                'title': 'Test Todo',
                'description': 'Test description',
                'priority': 'medium'
            }, follow_redirects=False)
            
            assert response.status_code == 302  # Still redirects even on error
            assert response.location.endswith('/')
    
    def test_toggle_todo_success(self, client):
        """Test GET /toggle/<id> successfully."""
        with patch('services.todo_service.todo_service.toggle_todo_completion'):
            response = client.get('/toggle/1', follow_redirects=False)
            
            assert response.status_code == 302  # Redirect after toggle
            assert response.location.endswith('/')
    
    def test_toggle_todo_server_error(self, client):
        """Test GET /toggle/<id> with server error."""
        with patch('services.todo_service.todo_service.toggle_todo_completion', side_effect=Exception("Server error")):
            response = client.get('/toggle/1', follow_redirects=False)
            
            assert response.status_code == 302  # Still redirects even on error
            assert response.location.endswith('/')
    
    def test_delete_todo_form_success(self, client):
        """Test GET /delete/<id> successfully."""
        with patch('services.todo_service.todo_service.delete_todo'):
            response = client.get('/delete/1', follow_redirects=False)
            
            assert response.status_code == 302  # Redirect after delete
            assert response.location.endswith('/')
    
    def test_delete_todo_form_server_error(self, client):
        """Test GET /delete/<id> with server error."""
        with patch('services.todo_service.todo_service.delete_todo', side_effect=Exception("Server error")):
            response = client.get('/delete/1', follow_redirects=False)
            
            assert response.status_code == 302  # Still redirects even on error
            assert response.location.endswith('/')


class TestRouteIntegration:
    """Test route integration with services."""
    
    def test_create_and_get_todo_integration(self, client):
        """Test creating a todo via API and retrieving it."""
        # Mock the service to simulate creating and retrieving
        created_todo = TodoModel(1, "Integration Test", "Test description", "high")
        
        with patch('models.todo.validate_todo_data', return_value=[]), \
             patch('services.todo_service.todo_service.create_todo', return_value=created_todo), \
             patch('services.todo_service.todo_service.get_all_todos', return_value=[created_todo.to_dict()]):
            
            # Create todo
            create_response = client.post('/api/todos', json={
                'title': 'Integration Test',
                'description': 'Test description',
                'priority': 'high'
            })
            assert create_response.status_code == 201
            
            # Get todos
            get_response = client.get('/api/todos')
            assert get_response.status_code == 200
            todos = get_response.get_json()
            assert len(todos) == 1
            assert todos[0]['title'] == 'Integration Test'
    
    def test_form_submission_data_handling(self, client):
        """Test that form submissions handle missing data gracefully."""
        with patch('services.todo_service.todo_service.validate_form_data', return_value=("Test Title", "medium")), \
             patch('services.todo_service.todo_service.create_todo'):
            
            # Test with minimal form data
            response = client.post('/add', data={'title': 'Test Title'}, follow_redirects=False)
            assert response.status_code == 302
    
    def test_api_content_type_handling(self, client):
        """Test API endpoints handle different content types."""
        # Test with JSON content type
        with patch('models.todo.validate_todo_data', return_value=['Title is required']):
            response = client.post('/api/todos', 
                                 data=json.dumps({}),
                                 content_type='application/json')
            assert response.status_code == 400
    
    def test_route_parameter_validation(self, client):
        """Test routes handle invalid parameters."""
        with patch('services.todo_service.todo_service.update_todo', return_value=None):
            # Test with invalid ID
            response = client.put('/api/todos/abc', json={'title': 'Test'})
            assert response.status_code == 404  # Flask handles invalid int conversion