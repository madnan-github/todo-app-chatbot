# Quickstart: Neon PostgreSQL + Better Auth Integration

**Feature**: 003-neon-better-auth
**Date**: 2025-12-30

## Prerequisites

1. **Neon Account**: Sign up at https://neon.tech (free tier)
2. **Neon Project**: Create a new project to get connection string
3. **Node.js 18+**: For frontend development
4. **Python 3.13+**: For backend development
5. **UV**: Python package manager

## Setup Steps

### 1. Get Neon Connection String

1. Log into Neon Console (https://console.neon.tech)
2. Select your project (or create new)
3. Go to **Dashboard** → **Connection Details**
4. Copy the connection string (format: `postgresql://user:pass@host/db`)

### 2. Configure Backend Environment

Create/update `backend/.env`:

```bash
# Database - Neon PostgreSQL (async driver)
DATABASE_URL=postgresql+asyncpg://neondb_owner:YOUR_PASSWORD@ep-xxx.us-east-1.aws.neon.tech/neondb?ssl=require

# JWT Configuration
JWT_SECRET_KEY=your-secret-key-at-least-32-chars
JWT_ALGORITHM=HS256
JWT_EXPIRY_DAYS=7

# CORS
CORS_ORIGINS=http://localhost:3000
```

**Note**: The `+asyncpg` in the URL is required for async SQLAlchemy.

### 3. Install Backend Dependencies

```bash
cd backend
uv add asyncpg  # Async PostgreSQL driver
uv remove aiosqlite  # Remove SQLite driver (optional cleanup)
```

### 4. Configure Frontend Environment

Update `frontend/.env.local`:

```bash
# API Configuration
NEXT_PUBLIC_API_URL=http://localhost:8000

# Better Auth (for future migration)
BETTER_AUTH_URL=http://localhost:3000
```

### 5. Start Development Servers

**Backend** (Terminal 1):
```bash
cd backend
uv run uvicorn src.main:app --reload --port 8000
```

**Frontend** (Terminal 2):
```bash
cd frontend
npm run dev
```

### 6. Verify Database Connection

Check backend logs for:
```
INFO:     Connected to Neon PostgreSQL
INFO:     Uvicorn running on http://127.0.0.1:8000
```

Test with curl:
```bash
curl http://localhost:8000/health
# Should return: {"status": "ok", "database": "connected"}
```

## Testing the Migration

### Test 1: Database Persistence

1. Create a user:
```bash
curl -X POST http://localhost:8000/api/v1/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "testpass123"}'
```

2. Stop the backend server (Ctrl+C)
3. Start it again
4. Verify user exists:
```bash
curl http://localhost:8000/api/v1/auth/signin \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "testpass123"}' \
  -c cookies.txt
```

### Test 2: Cookie-Based Authentication

1. Sign in (saves cookie):
```bash
curl -X POST http://localhost:8000/api/v1/auth/signin \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "testpass123"}' \
  -c cookies.txt -v
# Look for Set-Cookie: session_token=...
```

2. Access protected endpoint with cookie:
```bash
curl http://localhost:8000/api/v1/auth/session \
  -b cookies.txt
# Should return user and session info
```

3. Create task with cookie auth:
```bash
curl -X POST http://localhost:8000/api/v1/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Test task", "priority": "high"}' \
  -b cookies.txt
```

### Test 3: Cross-Origin Cookies (Browser)

1. Open http://localhost:3000
2. Sign in via the UI
3. Check browser DevTools → Application → Cookies
4. Verify `session_token` cookie exists for `localhost:8000`

## Common Issues

### Issue: "SSL SYSCALL error: EOF detected"

**Cause**: Neon compute suspended after inactivity
**Solution**: Enable `pool_pre_ping=True` in database.py:
```python
engine = create_async_engine(DATABASE_URL, pool_pre_ping=True)
```

### Issue: "Cookies not sent cross-origin"

**Cause**: CORS or fetch configuration
**Solution**:
1. Backend CORS must have `allow_credentials=True`
2. Frontend fetch must have `credentials: 'include'`

### Issue: "No module named 'asyncpg'"

**Cause**: Missing dependency
**Solution**: `uv add asyncpg`

### Issue: "Connection refused to Neon"

**Cause**: Incorrect connection string or SSL
**Solution**: Ensure URL has `?ssl=require` and correct credentials

## Rollback Procedure

If migration fails, revert to SQLite:

1. Restore `backend/.env`:
```bash
DATABASE_URL=sqlite+aiosqlite:///./todo_app.db
```

2. Restore dependencies:
```bash
cd backend
uv add aiosqlite
```

3. Restart backend server

## Next Steps

After successful migration:
1. Run `/sp.tasks` to generate implementation tasks
2. Follow TDD cycle: write tests → implement → verify
3. Commit changes on `003-neon-better-auth` branch
