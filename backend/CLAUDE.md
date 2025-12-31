# Backend Claude Code Rules

This file provides backend-specific guidance for Claude Code when working on the FastAPI backend.

## Technology Stack

- **Framework**: FastAPI 0.128+ (Python 3.13+)
- **ORM**: SQLModel (combines SQLAlchemy + Pydantic)
- **Database**: Neon PostgreSQL (serverless)
- **Authentication**: JWT with python-jose, passlib
- **Async Driver**: asyncpg

## Project Structure

```
backend/
├── src/
│   ├── __init__.py
│   ├── main.py            # FastAPI application entry point
│   ├── config.py          # Environment configuration
│   ├── database.py        # Database connection and session
│   ├── models.py          # SQLModel entities (User, Task, Tag, etc.)
│   ├── schemas.py         # Pydantic request/response schemas
│   ├── auth.py            # JWT verification middleware
│   └── routes/            # API route handlers
│       ├── __init__.py
│       ├── auth.py        # Authentication endpoints
│       └── tasks.py       # Task CRUD endpoints
├── tests/                 # Test files
├── pyproject.toml         # Project dependencies
└── .env.example           # Environment template
```

## Key Patterns

### Database Models (SQLModel)
- Define entities as SQLModel classes with `table=True`
- Use proper ForeignKey relationships for User-Task, Task-Tag
- Add indexes for frequently queried columns (user_id, status, priority, etc.)

### Pydantic Schemas
- Separate schemas for Create, Update, and Response operations
- Use Field validators for constraints (min_length, max_length, etc.)
- All Update schema fields should be Optional

### JWT Authentication
- Verify JWT token in Authorization header (Bearer scheme)
- Extract user_id from token claims
- Use dependency injection for protected routes

### User Isolation
- **CRITICAL**: Always filter by `user_id` from JWT token, NOT from request path
- Return 404 (not 403) for resources not found to avoid information leakage

## Environment Variables

Required in `.env`:
- `DATABASE_URL` - Neon PostgreSQL connection string
- `JWT_SECRET_KEY` - For token verification
- `JWT_ALGORITHM=HS256`
- `CORS_ORIGINS` - Allowed frontend origins

## Common Commands

```bash
# Development
uv run uvicorn src.main:app --reload  # Start dev server on port 8000

# Build & Production
uv run uvicorn src.main:app --host 0.0.0.0 --port 8000

# Database
uv run alembic upgrade head  # Run migrations (if using Alembic)
uv run python -c "from src.database import init_db; init_db()"  # Direct init

# Code Quality
uv run ruff check .          # Lint with ruff
uv run ruff format .         # Format with ruff
```

## API Endpoints

### Authentication
- `POST /api/v1/auth/signup` - Register new user
- `POST /api/v1/auth/signin` - Sign in user
- `POST /api/v1/auth/signout` - Sign out user
- `GET /api/v1/auth/me` - Get current user

### Tasks
- `GET /api/v1/tasks` - List user's tasks (with filters)
- `POST /api/v1/tasks` - Create new task
- `GET /api/v1/tasks/{task_id}` - Get specific task
- `PUT /api/v1/tasks/{task_id}` - Update task
- `DELETE /api/v1/tasks/{task_id}` - Delete task
- `PATCH /api/v1/tasks/{task_id}/complete` - Mark complete

### Tags
- `GET /api/v1/tags` - List user's tags
- `POST /api/v1/tags` - Create new tag
- `DELETE /api/v1/tags/{tag_id}` - Delete tag

## Available Skills

When working on backend tasks, check these skills first:
- `fastapi_project_setup` - Initial project setup
- `sqlmodel_schema_design` - Database models
- `pydantic_schema_creation` - Request/response validation
- `database_connection_setup` - Neon PostgreSQL connection
- `restful_api_design` - API endpoint patterns
- `jwt_verification` - JWT authentication
- `protected_route_implementation` - User isolation

## Related Documentation

- **Root CLAUDE.md**: Project-wide rules and agent guidelines
- **Frontend CLAUDE.md**: Next.js frontend patterns
- **specs/002-fullstack-web/**: Feature specifications and tasks
- **contracts/api-spec.yaml**: API contract specifications

---

*Adhere to all guidelines in the root CLAUDE.md for PHR creation and ADR suggestions.*
