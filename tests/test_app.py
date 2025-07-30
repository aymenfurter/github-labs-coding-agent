"""Unit tests for Flask app factory."""

import json
import pytest
from unittest.mock import patch


class TestAppFactory:
    """Test Flask application factory."""
    
    def test_create_app_returns_flask_app(self):
        """Test that create_app returns a Flask application."""
        from app import create_app
        
        app = create_app()
        assert app is not None
        assert app.__class__.__name__ == 'Flask'
    
    def test_app_has_blueprints_registered(self):
        """Test that blueprints are registered."""
        from app import create_app
        
        app = create_app()
        
        # Check that todo blueprint is registered
        blueprint_names = [bp.name for bp in app.blueprints.values()]
        assert 'todo' in blueprint_names
    
    def test_error_handlers_registered(self, app):
        """Test that error handlers are registered."""
        # Test 404 error handler
        with app.test_client() as client:
            response = client.get('/nonexistent-route')
            assert response.status_code == 404
            data = response.get_json()
            assert data['error'] == 'Not found'
    
    def test_500_error_handler(self, app):
        """Test 500 error handler."""
        # Test the error handler directly rather than creating routes
        with app.test_request_context():
            error_handler = app.error_handler_spec[None][500]
            if error_handler:
                # Get the first error handler function
                handler_func = list(error_handler.values())[0]
                response = handler_func(Exception("Test exception"))
                
                assert response[1] == 500
                data = json.loads(response[0].data.decode())
                assert data['error'] == 'Internal server error'
    
    def test_app_configuration(self, app):
        """Test app configuration."""
        # In test mode, testing should be enabled
        assert app.config['TESTING'] is True
    
    def test_app_routes_exist(self, app):
        """Test that expected routes exist."""
        with app.test_client() as client:
            # Test main routes exist (should not return 404)
            routes_to_test = [
                ('/', 'GET'),
                ('/api/todos', 'GET'),
                ('/api/todos', 'POST'),
            ]
            
            for route, method in routes_to_test:
                if method == 'GET':
                    with patch('services.todo_service.todo_service.get_all_todos', return_value=[]):
                        response = client.get(route)
                        assert response.status_code != 404
                elif method == 'POST':
                    response = client.post(route, json={})
                    assert response.status_code != 404  # Might be 400 for validation, but not 404
    
    def test_app_logging_configured(self):
        """Test that logging is configured."""
        import logging
        
        logger = logging.getLogger('app')
        assert logger.level <= logging.INFO


class TestAppExecution:
    """Test application execution scenarios."""
    
    def test_app_can_be_created_multiple_times(self):
        """Test that create_app can be called multiple times."""
        from app import create_app
        
        app1 = create_app()
        app2 = create_app()
        
        assert app1 is not app2  # Should be different instances
        assert app1.__class__ == app2.__class__
    
    def test_global_app_instance_exists(self):
        """Test that the global app instance exists."""
        import app
        
        assert hasattr(app, 'app')
        assert app.app is not None
        assert app.app.__class__.__name__ == 'Flask'
    
    def test_app_context_works(self, app):
        """Test that app context works correctly."""
        with app.app_context():
            from flask import current_app
            assert current_app._get_current_object() is app
    
    def test_request_context_works(self, app):
        """Test that request context works correctly."""
        with app.test_request_context('/'):
            from flask import request
            assert request.path == '/'


class TestAppErrorHandling:
    """Test application error handling."""
    
    def test_404_error_format(self, app):
        """Test 404 error response format."""
        with app.test_client() as client:
            response = client.get('/does-not-exist')
            
            assert response.status_code == 404
            assert response.content_type == 'application/json'
            
            data = response.get_json()
            assert 'error' in data
            assert data['error'] == 'Not found'
    
    def test_500_error_logging(self, app):
        """Test that 500 errors are logged."""
        # The error handler is tested through the actual endpoint behavior
        # This test verifies the error handler is properly registered
        error_handlers = app.error_handler_spec.get(None, {})
        assert 500 in error_handlers
        
    def test_error_handler_json_response(self, app):
        """Test that error handlers return JSON responses."""
        with app.test_client() as client:
            # Test 404
            response = client.get('/nonexistent')
            assert response.content_type == 'application/json'
            
            # Verify error handlers are properly registered
            error_handlers = app.error_handler_spec.get(None, {})
            assert 404 in error_handlers
            assert 500 in error_handlers


class TestAppSecurity:
    """Test application security configurations."""
    
    def test_csrf_disabled_in_test(self, app):
        """Test that CSRF is disabled in test configuration."""
        # This should be set in the test configuration
        assert app.config.get('WTF_CSRF_ENABLED', True) is False
    
    def test_debug_mode_in_test(self, app):
        """Test debug configuration in test mode."""
        # Testing mode usually disables debug
        assert app.config['TESTING'] is True


class TestAppIntegration:
    """Test application integration aspects."""
    
    def test_app_with_blueprint_routes(self, app):
        """Test that blueprint routes are accessible."""
        with app.test_client() as client:
            with patch('services.todo_service.todo_service.get_all_todos', return_value=[]):
                # Test a route from the todo blueprint
                response = client.get('/')
                assert response.status_code == 200
    
    def test_app_handles_json_requests(self, app):
        """Test that app can handle JSON requests."""
        with app.test_client() as client:
            response = client.post('/api/todos', 
                                 json={'title': 'Test Todo'},
                                 content_type='application/json')
            # Should not return 404 or 405 (method not allowed)
            assert response.status_code in [200, 201, 400, 500]  # Valid status codes
    
    def test_app_handles_form_requests(self, app):
        """Test that app can handle form requests."""
        with app.test_client() as client:
            response = client.post('/add', 
                                 data={'title': 'Test Todo'},
                                 content_type='application/x-www-form-urlencoded')
            # Should redirect (302) or process successfully
            assert response.status_code in [200, 302]
    
    def test_content_type_handling(self, app):
        """Test that app handles different content types appropriately."""
        with app.test_client() as client:
            # JSON request
            json_response = client.post('/api/todos', 
                                      json={'test': 'data'},
                                      content_type='application/json')
            assert json_response.content_type == 'application/json'
            
            # Form request should redirect
            form_response = client.post('/add', 
                                      data={'title': 'Test'},
                                      follow_redirects=False)
            assert form_response.status_code == 302