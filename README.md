# TaskFlow - Full-Stack Todo Application

A modern, full-stack todo application built with Next.js 15, FastAPI, and PostgreSQL.

## Features

- **User Authentication** - Sign up, sign in, and session management with JWT tokens
- **Task Management** - Create, read, update, and delete tasks
- **Priority Levels** - High, medium, and low priority with color indicators
- **Tags** - Organize tasks with custom tags and autocomplete
- **Search** - Find tasks by keyword in title or description
- **Filter** - Filter by status, priority, and tags
- **Sort** - Sort by creation date, priority, or title
- **Responsive Design** - Works on desktop, tablet, and mobile

## Tech Stack

### Frontend
- **Next.js 15+** with App Router
- **React 19** with TypeScript
- **Tailwind CSS** for styling
- **Better Auth** for authentication

### Backend
- **FastAPI** (Python 3.13+)
- **SQLModel** for database ORM
- **PostgreSQL** (Neon serverless)
- **JWT** for authentication

## Quick Start

### Prerequisites

- Node.js 18+ and npm
- Python 3.13+
- PostgreSQL database (Neon free tier recommended)

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Copy environment template
cp .env.local.example .env.local

# Edit .env.local with your configuration
# - NEXT_PUBLIC_API_URL: Your backend URL
# - BETTER_AUTH_SECRET: Generate a random secret

# Start development server
npm run dev
```

### Backend Setup

```bash
cd backend

# Install dependencies with UV
uv pip install -r pyproject.toml

# Copy environment template
cp .env.example .env

# Edit .env with your configuration:
# - DATABASE_URL: Your Neon PostgreSQL connection string
# - JWT_SECRET_KEY: Generate a secure random key
# - CORS_ORIGINS: Add your frontend URL

# Start development server
uv run uvicorn src.main:app --reload
```

### Environment Variables

#### Frontend (.env.local)
```
NEXT_PUBLIC_API_URL=http://localhost:8000
BETTER_AUTH_SECRET=your-secret-key-here
```

#### Backend (.env)
```
DATABASE_URL=postgresql://user:password@host:5432/database
JWT_SECRET_KEY=your-jwt-secret-key
JWT_ALGORITHM=HS256
CORS_ORIGINS=http://localhost:3000
ENVIRONMENT=development
```

## API Endpoints

### Authentication
- `POST /api/v1/auth/signup` - Register new user
- `POST /api/v1/auth/signin` - Sign in user

### Tasks
- `GET /api/v1/tasks` - List tasks (with filters, search, sort)
- `POST /api/v1/tasks` - Create task
- `GET /api/v1/tasks/{task_id}` - Get task details
- `PUT /api/v1/tasks/{task_id}` - Update task
- `DELETE /api/v1/tasks/{task_id}` - Delete task
- `PATCH /api/v1/tasks/{task_id}/complete` - Toggle completion

### Tags
- `GET /api/v1/tags` - List user's tags
- `POST /api/v1/tags` - Create new tag
- `DELETE /api/v1/tags/{tag_id}` - Delete tag

## Query Parameters

### GET /api/v1/tasks
| Parameter | Type | Description |
|-----------|------|-------------|
| `completed` | boolean | Filter by completion status |
| `priority` | string | Filter by priority (high, medium, low) - comma-separated for multiple |
| `tag_ids` | string | Filter by tag IDs - comma-separated |
| `search` | string | Search in title and description |
| `sort_by` | string | Sort field (created_at, updated_at, title, priority) |
| `sort_order` | string | Sort order (asc, desc) |
| `page` | number | Page number (default: 1) |
| `per_page` | number | Items per page (default: 20, max: 100) |

## Deployment

### Frontend (Vercel)

1. Connect your GitHub repository to Vercel
2. Configure build command: `npm run build`
3. Set environment variables in Vercel dashboard
4. Deploy

### Backend (Render/Railway)

1. Create a new Web Service
2. Connect your repository
3. Set build command: `pip install -r pyproject.toml`
4. Set start command: `uvicorn src.main:app`
5. Configure environment variables
6. Deploy

## Project Structure

```
todo-app-web/
├── frontend/                 # Next.js frontend
│   ├── app/                 # App Router pages
│   ├── components/          # React components
│   ├── hooks/               # Custom React hooks
│   ├── lib/                 # Utilities and configs
│   └── types/               # TypeScript types
├── backend/                  # FastAPI backend
│   ├── src/
│   │   ├── main.py          # Application entry point
│   │   ├── models.py        # SQLModel entities
│   │   ├── schemas.py       # Pydantic schemas
│   │   ├── routes/          # API route handlers
│   │   └── auth.py          # JWT authentication
│   └── pyproject.toml       # Python dependencies
└── specs/                    # Specifications
    └── 002-fullstack-web/   # Feature specs and tasks
```

## License

MIT
