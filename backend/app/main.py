from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import router
from src.routes.auth import router as auth_router
from src.routes.tasks import router as tasks_router
from src.routes.tags import router as tags_router
from src.routes.better_auth import router as better_auth_router, router_v1 as better_auth_v1_router
from .database import create_db_and_tables
from .mcp_server import start_mcp_server
from .logging_config import logger
import asyncio

app = FastAPI(title="Todo AI Chatbot API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include authentication routes
app.include_router(auth_router)
# Include task routes
app.include_router(tasks_router)
# Include tag routes
app.include_router(tags_router)
# Include Better Auth compatible routes
app.include_router(better_auth_router)  # Better Auth compatible endpoints at /api/auth
app.include_router(better_auth_v1_router)  # Better Auth compatible endpoints at /api/v1
# Include the main routes
app.include_router(router)

@app.on_event("startup")
def startup_event():
    """Initialize database tables on startup"""
    print("Initializing database tables...")
    create_db_and_tables()

    # Start MCP server in the background
    print("Starting MCP server...")
    start_mcp_server()

@app.get("/")
def read_root():
    return {"message": "Welcome to the Todo AI Chatbot API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)