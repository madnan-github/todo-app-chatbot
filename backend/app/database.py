from sqlmodel import create_engine, Session
from typing import Generator
from src.models import SQLModel
import os
from dotenv import load_dotenv

load_dotenv()

# Database URL from environment variables
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./todo_chatbot.db")

# For PostgreSQL, especially NeonDB, we need to handle connection parameters
if DATABASE_URL.startswith("postgresql://") or DATABASE_URL.startswith("postgres://"):
    # Parse the URL to check for existing sslmode parameter
    from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

    parsed_url = urlparse(DATABASE_URL)
    query_params = parse_qs(parsed_url.query)

    # Add sslmode if it doesn't exist
    if 'sslmode' not in query_params:
        query_params['sslmode'] = ['require']

    # Reconstruct the URL with updated query parameters
    new_query = urlencode(query_params, doseq=True)
    DATABASE_URL = urlunparse((
        parsed_url.scheme,
        parsed_url.netloc,
        parsed_url.path,
        parsed_url.params,
        new_query,
        parsed_url.fragment
    ))

# Create the engine
engine = create_engine(DATABASE_URL, echo=True)

def create_db_and_tables():
    """Create database tables"""
    SQLModel.metadata.create_all(engine)

def get_session() -> Generator[Session, None, None]:
    """Get database session"""
    with Session(engine) as session:
        yield session