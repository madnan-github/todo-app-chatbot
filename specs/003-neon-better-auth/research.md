# Research: Neon PostgreSQL + Better Auth Integration

**Feature**: 003-neon-better-auth
**Date**: 2025-12-30

## Decision 1: Database Driver for Neon PostgreSQL

**Decision**: Use SQLAlchemy async with asyncpg driver via `create_async_engine`

**Rationale**:
- SQLModel (already used) is built on SQLAlchemy and supports async operations
- asyncpg is the recommended async PostgreSQL driver for Python
- Neon documentation explicitly supports asyncpg connections
- Connection pooling via `pool_pre_ping=True` handles Neon's scale-to-zero behavior

**Alternatives Considered**:
- psycopg3 async: Good option but asyncpg has better performance benchmarks
- Raw asyncpg: Would require rewriting all database code, losing SQLModel benefits

**Implementation**:
```python
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

DATABASE_URL = "postgresql+asyncpg://user:pass@host/db?ssl=require"
engine = create_async_engine(DATABASE_URL, pool_pre_ping=True)
```

## Decision 2: Authentication Architecture

**Decision**: Keep FastAPI backend with custom JWT endpoints that are compatible with Better Auth client format

**Rationale**:
- Better Auth is a TypeScript/Node.js library - cannot run natively on FastAPI
- The Better Auth client expects specific API response formats which we can mimic
- Constitution specifies "Better Auth" but backend must remain FastAPI (constraint)
- Cookie-based JWT with HttpOnly is more secure than localStorage

**Alternatives Considered**:
- Full Better Auth (Node.js): Would require adding a separate Node auth server - adds complexity
- Keep localStorage JWT: Less secure, violates spec requirement for cookies
- Session tokens (database-stored): More complex, doesn't leverage existing JWT infrastructure

**Implementation**:
- Backend returns `{ user: {...}, session: { token: "..." } }` format
- Backend sets HttpOnly cookie with JWT token
- Frontend uses fetch with `credentials: 'include'` for cross-origin cookies
- Remove localStorage token handling from frontend

## Decision 3: Cookie Configuration for Cross-Origin

**Decision**: Use explicit CORS configuration with credentials and SameSite=Lax cookies

**Rationale**:
- Frontend (port 3000) and backend (port 8000) are different origins
- Cookies require `credentials: true` in CORS and `credentials: 'include'` in fetch
- SameSite=Lax allows cookies to be sent on top-level navigations
- SameSite=None would require HTTPS which complicates local development

**Implementation**:
```python
# Backend CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Cookie settings
response.set_cookie(
    key="session_token",
    value=jwt_token,
    httponly=True,
    samesite="lax",
    max_age=7 * 24 * 60 * 60,  # 7 days
    secure=False,  # True in production with HTTPS
)
```

## Decision 4: Neon Connection String Format

**Decision**: Use PostgreSQL+asyncpg connection string with SSL required

**Rationale**:
- Neon requires SSL connections (sslmode=require)
- asyncpg driver requires `postgresql+asyncpg://` prefix for SQLAlchemy
- Connection pooling with `pool_pre_ping=True` handles connection drops

**Connection String Format**:
```
postgresql+asyncpg://user:password@ep-xxx.us-east-1.aws.neon.tech/neondb?ssl=require
```

**Environment Variables**:
```
DATABASE_URL=postgresql+asyncpg://neondb_owner:password@ep-xxx.us-east-1.aws.neon.tech/neondb?ssl=require
```

## Decision 5: Session Persistence Strategy

**Decision**: JWT stored in HttpOnly cookie, verified on each request

**Rationale**:
- 7-day session persistence matches spec requirement
- HttpOnly prevents JavaScript access (XSS protection)
- JWT is self-contained - no database lookup needed for session verification
- Matches constitution principle VI (stateless design)

**Implementation**:
- Sign JWT with secret key and 7-day expiration
- Store in HttpOnly cookie named `session_token`
- Read from cookie on each request (not from Authorization header)
- Frontend auth client uses `credentials: 'include'` for all API calls

## Decision 6: Frontend Auth Client Approach

**Decision**: Custom auth hook that mimics Better Auth client patterns

**Rationale**:
- Better Auth client expects Node.js/Better Auth server endpoints
- FastAPI backend returns compatible format but different endpoint paths
- Custom hook provides same developer experience with FastAPI backend
- Can add Better Auth client library later if migrating to Node.js backend

**Implementation**:
```typescript
// Custom hook that works like Better Auth client
export function useAuth() {
  const signIn = async (email: string, password: string) => {
    const response = await fetch(`${API_URL}/api/v1/auth/signin`, {
      method: 'POST',
      credentials: 'include',  // Send cookies cross-origin
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password }),
    });
    // Cookie is automatically set by browser
  };

  const getSession = async () => {
    const response = await fetch(`${API_URL}/api/v1/auth/session`, {
      credentials: 'include',
    });
    return response.json();  // { user, session }
  };
}
```

## Files to Modify

### Backend
1. `backend/src/database.py` - Change to async PostgreSQL engine
2. `backend/src/config.py` - Update DATABASE_URL handling
3. `backend/src/routes/auth.py` - Add cookie-based session endpoints
4. `backend/src/auth.py` - Read JWT from cookies instead of headers
5. `backend/src/main.py` - Update CORS for credentials
6. `backend/pyproject.toml` - Add asyncpg dependency

### Frontend
1. `frontend/hooks/useAuth.tsx` - Update to use cookies (credentials: include)
2. `frontend/lib/api.ts` - Remove localStorage token, use credentials: include
3. `frontend/.env.local` - Update with Neon DATABASE_URL if needed

### Remove
1. localStorage token handling in frontend
2. SQLite-specific imports (aiosqlite)
3. Authorization header token injection

## Risk Assessment

| Risk | Mitigation |
|------|------------|
| Neon cold start latency | Use `pool_pre_ping=True` to handle reconnection |
| Cross-origin cookie issues | Explicit CORS config, test on localhost first |
| Session expiration handling | Frontend redirects to login on 401 |
| Data migration from SQLite | Fresh start acceptable per spec assumptions |
