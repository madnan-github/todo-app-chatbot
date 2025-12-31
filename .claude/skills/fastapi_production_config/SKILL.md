# Skill: FastAPI Production Configuration

Optimize FastAPI for production security, reliability, and cross-origin communication.

## Guidelines

- **CORS**: Implement `CORSMiddleware` using origins defined in `CORS_ORIGINS` environment variable.
- **Health Checks**: Implement a `/health` endpoint that returns 200 OK for basic readiness and optionally checks database connectivity.
- **Logging**: Use a production-grade logging configuration that outputs to stdout/stderr.
- **Security**: Ensure sensitive information like `JWT_SECRET` is read from environment variables and never hardcoded.

## Implementation Example

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.config import settings

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
```

## Acceptance Criteria

- [ ] `/health` endpoint is responsive.
- [ ] `CORSMiddleware` is configured with externalized origins.
- [ ] No hardcoded secrets.
