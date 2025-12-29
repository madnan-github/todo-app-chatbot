# syntax=docker/dockerfile:1

FROM python:3.13-slim

WORKDIR /app

# Install uv for fast package management
ENV UV_SYSTEM=1
RUN pip install uv

# Copy requirements and install dependencies
COPY pyproject.toml .
RUN uv pip install --system -r pyproject.toml

# Copy source code
COPY src ./src

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

# Run the application
CMD ["uv", "run", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
