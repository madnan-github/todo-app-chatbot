"""
MCP (Model Context Protocol) Server for Todo AI Chatbot
Implements the 5 required tool functions for the AI to manage tasks.
"""
from typing import Dict, Any, List, Optional
from src.models import Task, Conversation, Message
from .database import get_session
from sqlmodel import Session, select
from datetime import datetime


def add_task(user_id: str, title: str, description: Optional[str] = None) -> Dict[str, Any]:
    """
    Create a new task for a user
    """
    # In a real implementation, you'd use a database session
    # For now, simulating the operation

    # Create a mock task ID
    task_id = 1  # This would come from the database in a real implementation

    result = {
        "task_id": task_id,
        "status": "created",
        "title": title
    }

    print(f"[MCP] Created task {task_id} for user {user_id}: {title}")
    return result


def list_tasks(user_id: str, status: str = "all") -> List[Dict[str, Any]]:
    """
    Retrieve tasks for a user, optionally filtered by status
    """
    # In a real implementation, you'd query the database
    # For now, returning mock data

    # This would be: tasks = session.exec(select(Task).where(Task.user_id == user_id))
    # And then filter by status if needed

    mock_tasks = [
        {"id": 1, "title": "Buy groceries", "completed": False},
        {"id": 2, "title": "Walk the dog", "completed": True},
        {"id": 3, "title": "Finish report", "completed": False}
    ]

    # Filter based on status if specified
    if status == "pending":
        filtered_tasks = [task for task in mock_tasks if not task["completed"]]
    elif status == "completed":
        filtered_tasks = [task for task in mock_tasks if task["completed"]]
    else:  # all
        filtered_tasks = mock_tasks

    print(f"[MCP] Listed {len(filtered_tasks)} tasks for user {user_id} with status '{status}'")
    return filtered_tasks


def complete_task(user_id: str, task_id: int) -> Dict[str, Any]:
    """
    Mark a task as completed
    """
    # In a real implementation, you'd update the task in the database
    # For now, simulating the operation

    result = {
        "task_id": task_id,
        "status": "completed",
        "title": "Mock task title"  # In reality, you'd fetch this from the DB
    }

    print(f"[MCP] Completed task {task_id} for user {user_id}")
    return result


def delete_task(user_id: str, task_id: int) -> Dict[str, Any]:
    """
    Remove a task
    """
    # In a real implementation, you'd delete the task from the database
    # For now, simulating the operation

    result = {
        "task_id": task_id,
        "status": "deleted",
        "title": "Mock task title"  # In reality, you'd fetch this from the DB
    }

    print(f"[MCP] Deleted task {task_id} for user {user_id}")
    return result


def update_task(user_id: str, task_id: int, title: Optional[str] = None, description: Optional[str] = None) -> Dict[str, Any]:
    """
    Modify an existing task
    """
    # In a real implementation, you'd update the task in the database
    # For now, simulating the operation

    updated_title = title if title is not None else "Mock task title"

    result = {
        "task_id": task_id,
        "status": "updated",
        "title": updated_title
    }

    print(f"[MCP] Updated task {task_id} for user {user_id}")
    return result


# Placeholder for the actual MCP server implementation
# In a real implementation, you'd use the official MCP SDK to register these functions
def start_mcp_server():
    """
    Start the MCP server with the registered tool functions
    """
    print("[MCP] Starting MCP server...")
    print("[MCP] Registered tools: add_task, list_tasks, complete_task, delete_task, update_task")

    # In a real implementation, you'd use the MCP SDK to register the functions
    # For example: mcp.register_tool(add_task, ...)
    # And then start the server