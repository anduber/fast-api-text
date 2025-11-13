# Task Manager API (FastAPI)

A beginner-friendly, production-ready FastAPI project providing a simple task management API with full CRUD operations. It uses in-memory storage for simplicity, strong input validation with Pydantic, CORS middleware, basic security headers, and includes unit tests.

## Features
- CRUD tasks: create, list, retrieve, update, delete
- In-memory storage (no database) for easy onboarding
- Pydantic v2 validation and sanitation
- CORS middleware and security headers
- Environment-based configuration via `.env`
- Automatic docs: Swagger UI (`/docs`) and ReDoc (`/redoc`)
- Pytest + httpx unit tests

## Project Structure
```
task_manager_api/
├── .env.example
├── requirements.txt
├── README.md
├── main.py
├── app/
│   ├── __init__.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   └── security.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── task.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── task.py
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes/
│   │       ├── __init__.py
│   │       └── tasks.py
│   └── services/
│       ├── __init__.py
│       └── task_service.py
└── tests/
    ├── __init__.py
    ├── conftest.py
    └── test_tasks.py
```

## Prerequisites
- Python 3.11+ recommended
- Windows PowerShell, macOS Terminal, or Linux shell

## Virtual Environment Setup
Follow the steps for your OS to create and activate an isolated environment.

### Windows (PowerShell)
- `cd task_manager_api`
- `python -m venv .venv`
- `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`
- `.venv\Scripts\Activate.ps1`
- `pip install -r requirements.txt`

### macOS / Linux (bash/zsh)
- `cd task_manager_api`
- `python3 -m venv .venv`
- `source .venv/bin/activate`
- `pip install -r requirements.txt`

To deactivate later: `deactivate`

## Configuration
- Copy `.env.example` to `.env` and adjust values:
  - `APP_NAME`: Human-friendly name
  - `ENVIRONMENT`: `development` | `production` | `staging` | `test`
  - `DEBUG`: `true` or `false`
  - `ALLOWED_ORIGINS`: Comma-separated list or `*` in development

## Running the API
### Development
- `uvicorn main:app --reload --port 8000`
- Open Swagger UI: `http://localhost:8000/docs`
- Open ReDoc: `http://localhost:8000/redoc`

### Production (example)
- `uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4`
- Behind a reverse proxy (e.g., Nginx) with HTTPS and proper CORS origins

## API Endpoints
- `POST /tasks/` — create task
- `GET /tasks/` — list tasks
- `GET /tasks/{task_id}` — retrieve task
- `PUT /tasks/{task_id}` — update task (partial allowed)
- `DELETE /tasks/{task_id}` — delete task

## Request/Response Models
- `TaskCreate` — title, description?, is_completed?
- `TaskUpdate` — title?, description?, is_completed?
- `TaskRead` — id, title, description?, is_completed, created_at, updated_at

## Example Requests
- Create:
  - `curl -X POST http://localhost:8000/tasks/ -H "Content-Type: application/json" -d "{\"title\": \"Write docs\", \"description\": \"Document API\"}"`
- List:
  - `curl http://localhost:8000/tasks/`
- Get:
  - `curl http://localhost:8000/tasks/1`
- Update:
  - `curl -X PUT http://localhost:8000/tasks/1 -H "Content-Type: application/json" -d "{\"is_completed\": true}"`
- Delete:
  - `curl -X DELETE http://localhost:8000/tasks/1`

## Testing
- Activate your venv
- `pytest -q`

## Code Walkthrough
- `main.py`
  - Creates the FastAPI app, sets CORS and security headers, and includes routers.
- `app/core/config.py`
  - Loads `.env`, parses values into `Settings` using Pydantic, exposes `get_settings()`.
- `app/core/security.py`
  - Adds common security headers via middleware.
- `app/models/task.py`
  - Internal `Task` dataclass representing stored objects.
- `app/schemas/task.py`
  - Pydantic models (`TaskCreate`, `TaskUpdate`, `TaskRead`) with validation and sanitation.
- `app/services/task_service.py`
  - In-memory CRUD with `TaskNotFoundError` and `reset_store()` for tests.
- `app/api/routes/tasks.py`
  - CRUD endpoints, error handling to `HTTPException` with appropriate status codes.

## Notes & Best Practices
- Validate inputs: Pydantic enforces types and constraints; titles are trimmed.
- Error handling: 404 for missing tasks, 422 for validation errors (automatic).
- CORS: Use specific origins in production; avoid `*`.
- Security: Add authentication and rate limiting for production scenarios.
- Documentation: Swagger and ReDoc are enabled by default.

## Troubleshooting
- If `Activate.ps1` is blocked on Windows, ensure PowerShell execution policy allows scripts: `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`.
- If dependencies conflict, consider updating `requirements.txt` to newer compatible versions.