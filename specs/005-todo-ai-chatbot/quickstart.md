# Quickstart: Todo AI Chatbot

## Overview
Quick setup guide for the Todo AI Chatbot feature that allows users to manage tasks through natural language commands.

## Prerequisites
- Python 3.13+
- UV package manager
- PostgreSQL database (Neon recommended)
- OpenRouter API key
- Node.js 18+ (for frontend)

## Backend Setup

### 1. Environment Configuration
```bash
# Create .env file in backend root
DATABASE_URL=postgresql://username:password@localhost:5432/todo_chatbot
OPENROUTER_API_KEY=sk-or-xxxxxxxxxxxxxxxxxxxxxxx
SECRET_KEY=your-super-secret-key-here
```

### 2. Installation
```bash
cd backend
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install fastapi sqlmodel python-jose[cryptography] passlib[bcrypt] psycopg2-binary python-multipart python-dotenv openai
```

### 3. Database Setup
```bash
# Initialize database tables
python -c "
from app.database import engine
from app.models import Task, Conversation, Message
from sqlmodel import SQLModel

SQLModel.metadata.create_all(engine)
"
```

### 4. Run Backend Server
```bash
# Start the FastAPI server
uvicorn app.main:app --reload --port 8000
```

## Frontend Setup

### 1. Environment Configuration
```bash
# Create .env.local in frontend root
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
NEXT_PUBLIC_OPENAI_DOMAIN_KEY=your-domain-key-if-required
```

### 2. Installation
```bash
cd frontend
npm install
```

### 3. Run Frontend
```bash
npm run dev
```

## API Usage

### Send Message to Chatbot
```bash
curl -X POST http://localhost:8000/api/user123/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "message": "Add buy groceries"
  }'
```

### Response Example
```json
{
  "conversation_id": 456,
  "response": "✓ I added 'buy groceries' to your tasks",
  "tool_calls": [
    {
      "tool_name": "add_task",
      "result": {
        "task_id": 789,
        "status": "created",
        "title": "buy groceries"
      }
    }
  ]
}
```

## MCP Server Setup

### 1. Install MCP SDK
```bash
pip install @modelcontextprotocol/sdk
```

### 2. Start MCP Server
```bash
# Run the MCP server that exposes tools to the AI
python app/mcp_server.py
```

## Testing the Feature

### 1. Basic Task Creation
1. Send "Add buy groceries" to the chat endpoint
2. Verify task is created in the database
3. Confirm AI response acknowledges the creation

### 2. Task Listing
1. Send "Show my tasks" to the chat endpoint
2. Verify AI returns list of tasks
3. Confirm proper formatting of response

### 3. Task Completion
1. Send "Mark task 1 complete" to the chat endpoint
2. Verify task status updates in database
3. Confirm AI acknowledges completion

### 4. Conversation Persistence
1. Send multiple messages in sequence
2. Verify conversation history is maintained
3. Confirm AI can reference previous exchanges

## Troubleshooting

### Common Issues
- **API Rate Limits**: Check OpenRouter quota and implement retry logic
- **Authentication Errors**: Verify JWT token format and validity
- **Database Connection**: Ensure PostgreSQL is running and credentials are correct
- **CORS Issues**: Configure proper origins in FastAPI settings

### Debugging
- Enable debug logging in backend: `LOG_LEVEL=DEBUG`
- Check MCP server logs for tool execution issues
- Verify database connection with: `python -c "from app.database import engine; engine.connect(); print('Connected')"`