# Skill: Railway Deployment Configuration

Configure a FastAPI application for production deployment on Railway with dynamic port binding and process management.

## Guidelines

- **Port Binding**: Use `os.getenv("PORT", 8000)` to bind to the dynamic port assigned by Railway.
- **Procfile**: Create a `Procfile` at the root of the backend directory with: `web: uvicorn src.main:app --host 0.0.0.0 --port $PORT`.
- **Environment**: Use an `ENVIRONMENT` variable to toggle production features like strict CORS and logging.

## Implementation Example

```python
import os
from fastapi import FastAPI

app = FastAPI()

port = int(os.getenv("PORT", 8000))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.main:app", host="0.0.0.0", port=port)
```

## Acceptance Criteria

- [ ] `Procfile` exists and contains correct uvicorn command.
- [ ] Application binds to `$PORT` environment variable.
- [ ] Host is set to `0.0.0.0` for external accessibility.
