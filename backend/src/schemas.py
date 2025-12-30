"""Pydantic schemas for request/response validation."""
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, field_validator
from src.models import PriorityEnum


# ============================================================================
# User Schemas
# ============================================================================

class UserBase(BaseModel):
    """Base user schema with common fields."""
    email: str = Field(..., format="email", max_length=255)
    name: Optional[str] = Field(None, max_length=255)


class UserCreate(UserBase):
    """Schema for creating a new user."""
    password: str = Field(..., min_length=8, max_length=128)

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: str) -> str:
        if "@" not in v or "." not in v:
            raise ValueError("Invalid email format")
        return v.lower().strip()


class UserLogin(BaseModel):
    """Schema for user login."""
    email: str = Field(..., format="email")
    password: str = Field(..., min_length=1)


class UserResponse(UserBase):
    """Schema for user response (excludes sensitive data)."""
    id: str
    created_at: datetime

    class Config:
        from_attributes = True


# ============================================================================
# Tag Schemas
# ============================================================================

class TagBase(BaseModel):
    """Base tag schema."""
    name: str = Field(..., min_length=1, max_length=50)


class TagCreate(TagBase):
    """Schema for creating a tag."""
    pass


class TagResponse(TagBase):
    """Schema for tag response."""
    id: int
    user_id: str

    class Config:
        from_attributes = True


class TagListResponse(BaseModel):
    """Schema for paginated tag list."""
    tags: List[TagResponse]
    total: int
    page: int
    per_page: int


class TagAutocompleteResponse(BaseModel):
    """Schema for tag autocomplete response."""
    suggestions: List[str]


# ============================================================================
# Task Schemas
# ============================================================================

class TaskBase(BaseModel):
    """Base task schema."""
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    priority: PriorityEnum = Field(default=PriorityEnum.MEDIUM)


class TaskCreate(TaskBase):
    """Schema for creating a task."""
    tag_ids: Optional[List[int]] = None


class TaskUpdate(BaseModel):
    """Schema for updating a task (all fields optional)."""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    completed: Optional[bool] = None
    priority: Optional[PriorityEnum] = None
    tag_ids: Optional[List[int]] = None


class TaskResponse(TaskBase):
    """Schema for task response."""
    id: int
    user_id: str
    completed: bool
    created_at: datetime
    updated_at: datetime
    tags: List[TagResponse] = []

    class Config:
        from_attributes = True


class TaskListResponse(BaseModel):
    """Schema for paginated task list."""
    tasks: List[TaskResponse]
    total: int
    page: int
    per_page: int


# ============================================================================
# Auth Schemas
# ============================================================================

class SessionInfo(BaseModel):
    """Schema for session information."""
    token: str
    expiresAt: datetime

class BetterAuthUser(BaseModel):
    """Schema for user in Better Auth format."""
    id: str
    email: str
    name: Optional[str] = None

class BetterAuthResponse(BaseModel):
    """Schema for Better Auth response."""
    user: BetterAuthUser
    session: SessionInfo

class TokenResponse(BaseModel):
    """Schema for JWT token response."""
    access_token: str
    token_type: str = "bearer"
    expires_in: int


class AuthResponse(BaseModel):
    """Schema for authentication response."""
    user: UserResponse
    access_token: TokenResponse


# ============================================================================
# Error Schemas
# ============================================================================

class ErrorResponse(BaseModel):
    """Schema for error responses."""
    detail: str
    error_code: Optional[str] = None
