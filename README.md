# Todo Manager Application

A Flask-based todo management application with a clean architecture and comprehensive testing.

## Features

- Create, read, update, and delete todos
- Set priority levels (low, medium, high)
- Mark todos as completed
- Web interface and REST API
- Data persistence with JSON storage

## Architecture

The application follows a clean architecture pattern:

- **`models/`** - Data models and validation logic
- **`routes/`** - HTTP route handlers using Flask blueprints
- **`services/`** - Business logic and data operations
- **`templates/`** - HTML templates for the web interface
- **`static/`** - Static assets (CSS, JS, images)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd github-labs-coding-agent
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. For development, also install dev dependencies:
```bash
pip install -r requirements-dev.txt
```

## Usage

### Running the Application

```bash
python app.py
```

The application will start on `http://localhost:5000`.

### Using the Makefile

The project includes a Makefile for common development tasks:

```bash
make help          # Show available commands
make install       # Install dependencies
make run           # Run the application
make test          # Run all tests
make test-unit     # Run unit tests only
make test-integration  # Run integration tests only
make lint          # Run code linting
make format        # Format code with black
make coverage      # Run tests with coverage report
make clean         # Clean up generated files
```

## API Endpoints

- `GET /api/todos` - Get all todos
- `POST /api/todos` - Create a new todo
- `PUT /api/todos/<id>` - Update a todo
- `DELETE /api/todos/<id>` - Delete a todo

### Example API Usage

Create a todo:
```bash
curl -X POST http://localhost:5000/api/todos \
  -H "Content-Type: application/json" \
  -d '{"title": "Learn Python", "description": "Complete Python tutorial", "priority": "high"}'
```

Get all todos:
```bash
curl http://localhost:5000/api/todos
```

## Testing

The application has comprehensive test coverage including:

- **Unit Tests** - Test individual components in isolation
- **Integration Tests** - Test complete workflows and component interactions

### Running Tests

```bash
# Run all tests
python -m pytest

# Run with coverage
python -m pytest --cov=. --cov-report=html

# Run specific test categories
python -m pytest tests/unit/       # Unit tests only
python -m pytest tests/integration/  # Integration tests only
```

### Test Structure

```
tests/
├── conftest.py           # Test configuration and fixtures
├── unit/                 # Unit tests
│   ├── test_app.py       # App factory tests
│   ├── test_todo_model.py    # Model and validation tests
│   ├── test_todo_routes.py   # Route handler tests
│   └── test_todo_service.py  # Service layer tests
└── integration/          # Integration tests
    └── test_todo_app.py  # End-to-end workflow tests
```

## CI/CD

The project includes a GitHub Actions workflow (`.github/workflows/ci-cd.yml`) that:

- Runs tests on multiple Python versions (3.9, 3.10, 3.11, 3.12)
- Performs code quality checks (linting, formatting)
- Runs security scans
- Generates coverage reports
- Creates build artifacts

## Development

### Code Quality

The project uses several tools to maintain code quality:

- **pytest** - Testing framework
- **black** - Code formatting
- **flake8** - Code linting
- **coverage** - Test coverage reporting

### Project Configuration

- `pytest.ini` - Pytest configuration
- `.coveragerc` - Coverage reporting configuration
- `requirements.txt` - Production dependencies
- `requirements-dev.txt` - Development dependencies

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests: `make test`
5. Run linting: `make lint`
6. Format code: `make format`
7. Submit a pull request

## License

This project is licensed under the MIT License.