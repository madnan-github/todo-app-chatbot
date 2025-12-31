# Skill: Neon Database Production Setup

Configure SQLModel and SQLAlchemy with optimized connection pooling for Neon serverless PostgreSQL in production environments.

## Guidelines

- **Driver**: Always use `asyncpg` for asynchronous database operations.
- **Protocol**: The connection string must use `postgresql+asyncpg://`.
- **Pooling**: Configure `create_async_engine` with `pool_size` (e.g., 5) and `max_overflow` (e.g., 10) to manage connections efficiently in serverless environments.
- **SSL**: Ensure SSL mode is enabled or correctly handled by the driver for secure Neon connections.

## Implementation Example

```python
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel import SQLModel
from src.config import settings

# Optimized for serverless/ephemeral environments
engine = create_async_engine(
    settings.DATABASE_URL.replace("postgres://", "postgresql+asyncpg://"),
    pool_size=settings.DB_POOL_SIZE,
    max_overflow=settings.DB_MAX_OVERFLOW,
    pool_pre_ping=True
)
```

## Acceptance Criteria

- [ ] Connection string uses `postgresql+asyncpg://`.
- [ ] Connection pooling parameters are explicitly defined.
- [ ] `pool_pre_ping` is enabled to handle stale connections.
