---
id: 001
title: Create Todo AI Chatbot Feature Specification
stage: spec
date_iso: 2026-01-13
surface: agent
model: claude-opus-4-5-20251101
feature: todo-ai-chatbot
branch: 005-todo-ai-chatbot
user: ruser
command: /sp.specify
labels: ["specification", "todo-chatbot", "ai-tools", "natural-language"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml: |
  - specs/005-todo-ai-chatbot/spec.md
  - specs/005-todo-ai-chatbot/checklists/requirements.md
tests_yaml: |
  - "Validate spec against quality checklist"
  - "Verify all user scenarios are testable"
  - "Confirm success criteria are measurable"
---

# Create Todo AI Chatbot Feature Specification

## PROMPT_TEXT

# Phase III: Todo AI Chatbot - Implementation Spec

## 🎯 What We're Building

A chatbot where users can manage their todo tasks by typing natural language commands. Example:
- User says: "Add buy groceries"
- AI creates the task
- User says: "Show my pending tasks"
- AI lists them
- User says: "Mark task 1 complete"
- AI marks it done

## 🏗️ Simple Architecture

```
User → ChatKit UI → FastAPI Backend → OpenRouter API (Claude) → MCP Server → Database
```

1. **ChatKit**: Pretty UI where user types messages (OpenAI's chat library)
2. **FastAPI**: Receives messages, calls AI, runs tools, saves to database
3. **OpenRouter**: AI brain using Claude (not OpenAI direct, saves money)
4. **MCP Server**: Tool handler (add task, list tasks, etc.)
5. **Database**: Stores tasks and conversation history (PostgreSQL)

---

## 📦 Technology Stack

| Part | Tool |
|------|------|
| Frontend UI | OpenAI ChatKit |
| Backend API | FastAPI (Python) |
| AI Model | OpenRouter API (Claude) |
| Task Tools | MCP Server |
| Database | PostgreSQL (Neon) |
| ORM | SQLModel |
| Auth | Better Auth |

---

## 💾 Database (3 Simple Tables)

### Task Table
```
id, user_id, title, description, completed (true/false), created_at, updated_at
```

### Conversation Table
```
id, user_id, created_at, updated_at
```

### Message Table
```
id, user_id, conversation_id, role (user or assistant), content, created_at
```

---

## 🤖 MCP Tools (5 Simple Functions)

These are the "tools" the AI can use to manage tasks.

### 1. add_task
- **What it does**: Create a new task
- **Input**: `user_id`, `title`, `description` (optional)
- **Output**: `{"task_id": 5, "status": "created", "title": "Buy groceries"}`

### 2. list_tasks
- **What it does**: Show all/pending/completed tasks
- **Input**: `user_id`, `status` (optional: "all" or "pending" or "completed")
- **Output**: `[{"id": 1, "title": "Buy groceries", "completed": false}, ...]`

### 3. complete_task
- **What it does**: Mark a task as done
- **Input**: `user_id`, `task_id`
- **Output**: `{"task_id": 3, "status": "completed", "title": "Call mom"}`

### 4. delete_task
- **What it does**: Remove a task
- **Input**: `user_id`, `task_id`
- **Output**: `{"task_id": 2, "status": "deleted", "title": "Old task"}`

### 5. update_task
- **What it does**: Change task title or description
- **Input**: `user_id`, `task_id`, `title` (optional), `description` (optional)
- **Output**: `{"task_id": 1, "status": "updated", "title": "New title"}`

---

## 🔄 How Each Request Works

When user sends a message:

1. **Get History**: Fetch all previous messages for this conversation from database
2. **Send to AI**: Call OpenRouter API with message + history + available tools
3. **AI Decides**: Claude reads message and picks which tool(s) to use
4. **Run Tool**: Execute the MCP tool (add_task, list_tasks, etc.)
5. **Get Result**: Tool returns data (new task created, list of tasks, etc.)
6. **AI Responds**: Claude writes a friendly message back using the tool results
7. **Save Everything**: Store both user message and AI response in database
8. **Return to User**: Send AI's response + tool results back to ChatKit

---

## 💬 Natural Language Examples

What the AI should understand:

| User Says | Tool Used | Action |
|-----------|-----------|--------|
| "Add buy groceries" | add_task | Creates task "buy groceries" |
| "Show my tasks" | list_tasks | Shows all tasks |
| "What's pending?" | list_tasks (pending) | Shows incomplete tasks |
| "Mark task 3 done" | complete_task | Marks task 3 complete |
| "Delete the meeting" | delete_task | Deletes task |
| "Change task 1 to Pay bills" | update_task | Updates task 1 title |
| "What did I finish?" | list_tasks (completed) | Shows done tasks |

---

## 🌐 Frontend (ChatKit)

### Setup
1. Create React/Next.js app with OpenAI ChatKit library
2. Set environment variables:
   - `NEXT_PUBLIC_API_BASE_URL` = your backend URL (e.g., http://localhost:8000)
   - `NEXT_PUBLIC_OPENAI_DOMAIN_KEY` = get from OpenAI after domain allowlist

3. ChatKit shows chat messages, user types, AI responds

### Domain Allowlist (Production Only)
1. Deploy your frontend to a real URL (Vercel, etc.)
2. Go to: https://platform.openai.com/settings/organization/security/domain-allowlist
3. Add your domain (e.g., https://my-app.vercel.app)
4. Copy the domain key and add to `.env.local`
5. ChatKit will work on that domain in production

### Local Development
- `localhost` works without domain allowlist during development
- Domain key only needed for production deployment

---

## 🖥️ Backend (FastAPI)

### Main Endpoint

**POST** `/api/{user_id}/chat`

**Receives:**
```json
{
  "conversation_id": 123,  // optional, creates new if missing
  "message": "Add buy groceries"
}
```

**Returns:**
```json
{
  "conversation_id": 123,
  "response": "✓ I added 'buy groceries' to your tasks",
  "tool_calls": [
    {
      "tool_name": "add_task",
      "result": {"task_id": 5, "status": "created", "title": "buy groceries"}
    }
  ]
}
```

### Processing Steps
1. Get user from auth token
2. If no conversation_id, create new conversation
3. Fetch last 20 messages from database
4. Call OpenRouter with: messages + MCP tools available
5. Parse AI response and any tool calls
6. Run each tool against database
7. Store user message in database
8. Store AI response in database
9. Return JSON response

### Environment Variables
```
DATABASE_URL=postgresql://...  # Neon database
OPENROUTER_API_KEY=sk_...      # OpenRouter API key
```

---

## 🛠️ OpenRouter API Setup

### Why OpenRouter?
- Works like OpenAI API but cheaper
- Pay as you go (no subscription)
- Access to Claude, GPT-4, and more
- No monthly commitment for hackathons

### How to Use
1. Go to https://openrouter.ai
2. Sign up free
3. Generate API key
4. Fund account ($5-10 to start)
5. Add to backend `.env`: `OPENROUTER_API_KEY=...`

### OpenRouter vs OpenAI
- **OpenAI ChatKit** = Frontend UI (what user sees)
- **OpenRouter** = Backend AI (what we use instead of OpenAI API)
- ChatKit doesn't care which LLM you use (hidden from ChatKit)

---

## 📁 Folder Structure

```
project/
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   └── ChatKitWrapper.tsx
│   │   └── App.tsx
│   └── .env.local
│
├── backend/
│   ├── app/
│   │   ├── models.py          # Task, Conversation, Message tables
│   │   ├── database.py        # Database connection
│   │   ├── routes.py          # /api/{user_id}/chat endpoint
│   │   └── openrouter_agent.py # Call OpenRouter API
│   ├── mcp_server.py          # MCP tools (add_task, list_tasks, etc.)
│   └── .env
│
└── README.md
```

---

## ✅ Success Checklist

- [ ] Database tables created (Task, Conversation, Message)
- [ ] MCP server running with all 5 tools
- [ ] FastAPI `/api/{user_id}/chat` endpoint working
- [ ] OpenRouter API integration complete
- [ ] ChatKit frontend shows messages
- [ ] Can add task by typing "add buy milk"
- [ ] Can list tasks by typing "show my tasks"
- [ ] Can mark task complete by typing "mark task 1 done"
- [ ] Can delete task by typing "delete task 2"
- [ ] Can update task by typing "change task 1 to pay bills"
- [ ] Conversation history persists (database saves messages)
- [ ] Messages load when reopening conversation
- [ ] Server restart doesn't lose data
- [ ] Authentication prevents seeing other users' tasks
- [ ] Domain allowlist configured for production

---

## 🚀 Quick Start

1. **Setup Database**: Create PostgreSQL database at Neon
2. **Setup OpenRouter**: Get API key at openrouter.ai
3. **Setup Backend**:
   - Install Python dependencies
   - Create `.env` with DATABASE_URL and OPENROUTER_API_KEY
   - Run FastAPI server (`python -m uvicorn app.main:app --reload`)
   - Start MCP server
4. **Setup Frontend**:
   - Install Node.js dependencies
   - Create `.env.local` with API_BASE_URL
   - Run `npm run dev`
5. **Test**: Type "Add test task" in ChatKit and see it appear

---

## 🎯 Key Points to Remember

- ✅ ChatKit = UI only (doesn't care about OpenRouter)
- ✅ OpenRouter = LLM (replaces OpenAI API, saves money)
- ✅ Server holds NO state (everything in database)
- ✅ Each request fetches history from DB and processes fresh
- ✅ MCP tools are simple database operations (no AI logic)
- ✅ AI (Claude via OpenRouter) decides which tools to use
- ✅ Domain allowlist required only for production ChatKit
- ✅ Keep OpenRouter API key secret (backend only)
- ✅ User isolation: users can only see their own tasks

---

## 🔐 Security

- Use Better Auth for user authentication
- Store OpenRouter API key in backend `.env` (never in frontend)
- Each request validates user_id matches auth token
- Users can only access their own tasks and conversations
- Database queries filtered by user_id automatically

---

## 📝 AI Instructions (System Prompt)

The AI should be told:

> You are a helpful todo assistant. Users tell you what to do with their tasks.
>
> You have 5 tools:
> 1. add_task - create new task
> 2. list_tasks - show tasks
> 3. complete_task - mark done
> 4. delete_task - remove task
> 5. update_task - change task
>
> When user says "add buy milk", use add_task.
> When they say "show tasks", use list_tasks.
> When they say "done with task 1", use complete_task.
> Always confirm what you did: "✓ Added 'buy milk' to your tasks"

## RESPONSE_TEXT

Successfully created the feature specification for the Todo AI Chatbot. The specification includes:

- User scenarios with prioritized user stories (Natural Language Task Management, Conversation Persistence, Advanced Task Operations)
- Comprehensive functional requirements (FR-001 to FR-015)
- Key entities (Task, Conversation, Message)
- Measurable success criteria (SC-001 to SC-006)
- Edge cases identification

The specification follows all quality criteria:
- No implementation details (languages, frameworks, APIs)
- Focused on user value and business needs
- Written for non-technical stakeholders
- All requirements are testable and unambiguous
- Success criteria are measurable and technology-agnostic

The feature branch 005-todo-ai-chatbot has been created with the specification file at specs/005-todo-ai-chatbot/spec.md and a quality checklist at specs/005-todo-ai-chatbot/checklists/requirements.md. The specification is ready for the next phase (/sp.clarify or /sp.plan).