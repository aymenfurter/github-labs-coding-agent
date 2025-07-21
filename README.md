# Todo Manager

A modern, feature-rich Todo Manager web application built with Flask. This application provides both a clean web interface and a REST API for managing your tasks efficiently.

![Todo Manager Screenshot](https://github.com/user-attachments/assets/cb0ab247-ee16-46ef-a4b0-0818e07fafaa)

## Features

### ✨ Core Functionality
- **Create, Read, Update, Delete (CRUD)** operations for todos
- **Priority levels**: Low, Medium, High
- **Task completion tracking** with toggle functionality
- **Persistent storage** using JSON files
- **Input validation** and error handling
- **Real-time statistics** (total, pending, completed tasks)

### 🎨 User Interface
- **Modern, responsive web interface**
- **Interactive form** for adding new todos
- **Filter system** (All, Pending, Completed, High Priority)
- **Modal-based editing** with inline updates
- **Visual priority indicators** and completion status
- **Font Awesome icons** for enhanced UX

### 🔌 API Endpoints
- **RESTful API** for programmatic access
- **JSON responses** for all API endpoints
- **Comprehensive error handling** with proper HTTP status codes

## Requirements

- **Python 3.12+**
- **Flask 2.3.3**
- **Werkzeug 2.3.7**

## Installation

### Using Dev Container (Recommended)
This project includes a dev container configuration for easy setup:

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd github-labs-coding-agent
   ```

2. **Open in VS Code with Dev Containers extension**:
   - Install the [Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)
   - Open the project in VS Code
   - When prompted, click "Reopen in Container"

### Manual Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd github-labs-coding-agent
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Starting the Application

```bash
python app.py
```

The application will start on `http://localhost:5000` by default.

### Web Interface

1. **Navigate** to `http://localhost:5000` in your browser
2. **Add todos** using the form at the top of the page
3. **Manage todos** with the action buttons:
   - ✅ **Toggle completion** status
   - ✏️ **Edit** todo details
   - 🗑️ **Delete** todos
4. **Filter todos** using the filter buttons (All, Pending, Completed, High Priority)

### API Usage

The application provides a REST API for programmatic access:

#### Get All Todos
```bash
GET /api/todos
```

**Response**:
```json
[
  {
    "id": 1,
    "title": "Sample Todo",
    "description": "This is a sample todo",
    "completed": false,
    "created_at": "2025-07-21T16:04:30.123456",
    "priority": "medium"
  }
]
```

#### Create a New Todo
```bash
POST /api/todos
Content-Type: application/json

{
  "title": "New Task",
  "description": "Task description",
  "priority": "high"
}
```

**Response**: `201 Created`
```json
{
  "id": 2,
  "title": "New Task",
  "description": "Task description",
  "completed": false,
  "created_at": "2025-07-21T16:04:30.123456",
  "priority": "high"
}
```

#### Update a Todo
```bash
PUT /api/todos/{id}
Content-Type: application/json

{
  "title": "Updated Task",
  "completed": true,
  "priority": "low"
}
```

**Response**: `200 OK`
```json
{
  "id": 2,
  "title": "Updated Task",
  "description": "Task description",
  "completed": true,
  "created_at": "2025-07-21T16:04:30.123456",
  "priority": "low"
}
```

#### Delete a Todo
```bash
DELETE /api/todos/{id}
```

**Response**: `200 OK`
```json
{
  "message": "Todo deleted successfully"
}
```

### Data Validation

The application includes comprehensive input validation:

- **Title**: Required, maximum 200 characters
- **Description**: Optional, maximum 1000 characters  
- **Priority**: Must be one of: `low`, `medium`, `high`
- **Completed**: Boolean value

## Project Structure

```
github-labs-coding-agent/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── .gitignore            # Git ignore rules
├── .devcontainer/        # Dev container configuration
│   └── devcontainer.json
├── models/               # Data models
│   ├── __init__.py
│   └── todo.py          # Todo model and validation
├── routes/               # Route handlers
│   ├── __init__.py
│   └── todo_routes.py   # Todo route definitions
├── services/             # Business logic layer
│   ├── __init__.py
│   └── todo_service.py  # Todo service operations
├── templates/            # HTML templates
│   ├── base.html        # Base template
│   └── index.html       # Main page template
└── static/              # Static assets
    ├── css/             # Stylesheets
    └── js/              # JavaScript files
```

## Architecture

The application follows a **layered architecture** pattern:

- **Routes Layer** (`routes/`): Handles HTTP requests and responses
- **Service Layer** (`services/`): Contains business logic and data operations
- **Model Layer** (`models/`): Defines data structures and validation rules
- **Persistence Layer**: JSON file storage (`todos.json`)

### Key Design Patterns

- **Blueprint Pattern**: Modular route organization
- **Application Factory Pattern**: Flexible app configuration
- **Service Layer Pattern**: Separation of business logic
- **Model-View-Controller (MVC)**: Clear separation of concerns

## Development

### Features

- **Comprehensive logging** with configurable levels
- **Error handling** with custom error pages (404, 500)
- **Input sanitization** and validation
- **Debug mode** for development
- **Auto-reloading** during development

### File Storage

Todos are stored in `todos.json` with the following structure:
```json
{
  "todos": [
    {
      "id": 1,
      "title": "Sample Todo",
      "description": "Description",
      "completed": false,
      "created_at": "2025-07-21T16:04:30.123456",
      "priority": "medium"
    }
  ],
  "next_id": 2
}
```

### Contributing

1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b feature-name`
3. **Make** your changes
4. **Test** your changes thoroughly
5. **Submit** a pull request

### Error Handling

The application includes robust error handling:
- **400 Bad Request**: Invalid input data
- **404 Not Found**: Todo not found
- **500 Internal Server Error**: Server-side errors

All errors return JSON responses with descriptive error messages.

## License

This project is open source. Please check the repository for license details.

## Support

For issues, questions, or contributions, please use the GitHub repository's issue tracker.