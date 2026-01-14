"""SQLModel database entities."""
from datetime import datetime
from enum import Enum
from typing import Optional, TYPE_CHECKING, List
from sqlmodel import Field, SQLModel, Relationship

if TYPE_CHECKING:
    pass


class PriorityEnum(str, Enum):
    """Task priority levels."""
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


# Define TaskTag first since it's used as link_model
class TaskTag(SQLModel, table=True):
    """Junction table for Task-Tag many-to-many relationship."""
    task_id: Optional[int] = Field(foreign_key="task.id", primary_key=True, default=None)
    tag_id: Optional[int] = Field(foreign_key="tag.id", primary_key=True, default=None)


class User(SQLModel, table=True):
    """User entity managed by Better Auth."""
    __table_args__ = {'extend_existing': True}

    id: str = Field(primary_key=True, max_length=255)
    email: str = Field(unique=True, max_length=255)
    password_hash: str = Field(max_length=255)
    name: Optional[str] = Field(max_length=255, default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    tasks: list["Task"] = Relationship(back_populates="user")
    tags: list["Tag"] = Relationship(back_populates="user")


class Task(SQLModel, table=True):
    """Task entity representing a todo item."""
    __table_args__ = {'extend_existing': True}

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(foreign_key="user.id", nullable=False, index=True)
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = Field(max_length=1000, default=None)
    completed: bool = Field(default=False, index=True)
    priority: PriorityEnum = Field(default=PriorityEnum.MEDIUM, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    user: "User" = Relationship(back_populates="tasks")
    tags: list["Tag"] = Relationship(
        back_populates="tasks",
        link_model=TaskTag
    )


class Tag(SQLModel, table=True):
    """Tag entity for task categorization."""
    __table_args__ = {'extend_existing': True}

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(foreign_key="user.id", nullable=False, index=True)
    name: str = Field(min_length=1, max_length=50)

    # Relationships
    user: "User" = Relationship(back_populates="tags")
    tasks: list["Task"] = Relationship(
        back_populates="tags",
        link_model=TaskTag
    )


class Conversation(SQLModel, table=True):
    """Conversation entity for chat history."""
    __table_args__ = {'extend_existing': True}

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship to messages
    messages: List["Message"] = Relationship(back_populates="conversation")


class Message(SQLModel, table=True):
    """Message entity for chat history."""
    __table_args__ = {'extend_existing': True}

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True)
    conversation_id: int = Field(foreign_key="conversation.id", index=True)
    role: str = Field(regex="^(user|assistant)$")
    content: str = Field(max_length=10000)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship to conversation
    conversation: "Conversation" = Relationship(back_populates="messages")
