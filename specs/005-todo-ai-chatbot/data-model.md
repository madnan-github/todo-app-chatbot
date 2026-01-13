# Data Model: Todo AI Chatbot

## Overview
Data model for the Todo AI Chatbot feature, defining the structure of Task, Conversation, and Message entities.

## Entities

### 1. Task
Represents a user's todo item that can be managed through natural language commands.

**Fields**:
- `id` (Integer): Primary key, auto-incrementing
- `user_id` (String): Foreign key linking to user, ensures user isolation
- `title` (String): Task title/description from user input
- `description` (String, Optional): Additional details about the task
- `completed` (Boolean): Whether the task is marked as complete
- `created_at` (DateTime): Timestamp when task was created
- `updated_at` (DateTime): Timestamp when task was last updated

**Relationships**:
- Belongs to one user (many-to-one with user table)
- No direct relationships to other entities

**Validation Rules**:
- `title` must be between 1-255 characters
- `user_id` must reference a valid user
- `completed` defaults to false
- `created_at` is set automatically on creation
- `updated_at` is updated automatically on modification

**State Transitions**:
- `completed` can transition from `false` to `true` (complete_task operation)
- `completed` can transition from `true` to `false` (update_task operation)
- All fields except `completed` can be modified via update_task operation

### 2. Conversation
Represents a thread of messages between a user and the AI assistant.

**Fields**:
- `id` (Integer): Primary key, auto-incrementing
- `user_id` (String): Foreign key linking to user
- `created_at` (DateTime): Timestamp when conversation was started
- `updated_at` (DateTime): Timestamp when conversation was last updated

**Relationships**:
- Belongs to one user (many-to-one with user table)
- Has many Messages (one-to-many relationship)

**Validation Rules**:
- `user_id` must reference a valid user
- `created_at` is set automatically on creation
- `updated_at` is updated automatically when new messages are added

### 3. Message
Represents individual messages in a conversation between user and AI.

**Fields**:
- `id` (Integer): Primary key, auto-incrementing
- `user_id` (String): Foreign key linking to user
- `conversation_id` (Integer): Foreign key linking to conversation
- `role` (String): Role of the message sender ('user' or 'assistant')
- `content` (Text): The actual message content
- `created_at` (DateTime): Timestamp when message was created

**Relationships**:
- Belongs to one user (many-to-one with user table)
- Belongs to one conversation (many-to-one with conversation table)

**Validation Rules**:
- `user_id` must reference a valid user
- `conversation_id` must reference a valid conversation
- `role` must be either 'user' or 'assistant'
- `content` must be between 1-10000 characters
- `created_at` is set automatically on creation

**Constraints**:
- Messages must belong to conversations owned by the same user
- User messages should be associated with the user who owns the conversation
- Assistant messages should be associated with the user who owns the conversation

## Database Schema (SQLModel)

```python
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional, List

class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True)
    title: str = Field(min_length=1, max_length=255)
    description: Optional[str] = Field(default=None)
    completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class Conversation(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship to messages
    messages: List["Message"] = Relationship(back_populates="conversation")

class Message(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True)
    conversation_id: int = Field(foreign_key="conversation.id", index=True)
    role: str = Field(regex="^(user|assistant)$")
    content: str = Field(max_length=10000)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship to conversation
    conversation: Conversation = Relationship(back_populates="messages")
```

## Indexes

For performance optimization:

1. **Task table**:
   - Index on `user_id` for efficient user-based queries
   - Composite index on `(user_id, completed)` for filtered queries

2. **Conversation table**:
   - Index on `user_id` for efficient user-based queries

3. **Message table**:
   - Index on `user_id` for efficient user-based queries
   - Index on `conversation_id` for efficient conversation-based queries
   - Composite index on `(conversation_id, created_at)` for chronological ordering

## Data Flow

1. **New Task Creation**: User sends "Add buy groceries" → AI calls add_task → Task created with completed=false
2. **Task Listing**: User sends "Show my tasks" → AI calls list_tasks → Tasks retrieved for user
3. **Task Completion**: User sends "Mark task 1 done" → AI calls complete_task → Task updated with completed=true
4. **Conversation Flow**: User message stored in Message table → AI response stored in Message table → Conversation updated_at timestamp refreshed