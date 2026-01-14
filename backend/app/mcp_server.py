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
    # Get a database session and create the task
    with next(get_session()) as session:
        task = Task(
            user_id=user_id,
            title=title,
            description=description,
            completed=False
        )
        session.add(task)
        session.commit()
        session.refresh(task)  # Refresh to get the auto-generated ID

        result = {
            "task_id": task.id,
            "status": "created",
            "title": task.title,
            "description": task.description
        }

        print(f"[MCP] Created task {task.id} for user {user_id}: {title}")
        return result


def list_tasks(user_id: str, status: str = "all") -> List[Dict[str, Any]]:
    """
    Retrieve tasks for a user, optionally filtered by status
    """
    # Get a database session and query tasks
    with next(get_session()) as session:
        # Build the query based on the status filter
        query = select(Task).where(Task.user_id == user_id)

        if status == "pending":
            query = query.where(Task.completed == False)
        elif status == "completed":
            query = query.where(Task.completed == True)

        # Execute the query
        tasks = session.exec(query).all()

        # Convert to dictionary format
        task_list = []
        for task in tasks:
            task_dict = {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "completed": task.completed,
                "priority": task.priority.value if task.priority else "medium"
            }
            task_list.append(task_dict)

        print(f"[MCP] Listed {len(task_list)} tasks for user {user_id} with status '{status}'")
        return task_list


def complete_task(user_id: str, task_id: int) -> Dict[str, Any]:
    """
    Mark a task as completed
    """
    # Get a database session and update the task
    with next(get_session()) as session:
        # Find the task for the specific user
        task = session.exec(
            select(Task).where(Task.id == task_id, Task.user_id == user_id)
        ).first()

        if task:
            task.completed = True
            session.add(task)
            session.commit()
            session.refresh(task)

            result = {
                "task_id": task.id,
                "status": "completed",
                "title": task.title
            }

            print(f"[MCP] Completed task {task.id} for user {user_id}")
            return result
        else:
            # Task not found for this user
            print(f"[MCP] Could not find task {task_id} for user {user_id}")
            return {
                "task_id": task_id,
                "status": "not_found",
                "title": "Task not found"
            }


def delete_task(user_id: str, task_id: int) -> Dict[str, Any]:
    """
    Remove a task
    """
    # Get a database session and delete the task
    with next(get_session()) as session:
        # Find the task for the specific user
        task = session.exec(
            select(Task).where(Task.id == task_id, Task.user_id == user_id)
        ).first()

        if task:
            session.delete(task)
            session.commit()

            result = {
                "task_id": task.id,
                "status": "deleted",
                "title": task.title
            }

            print(f"[MCP] Deleted task {task.id} for user {user_id}")
            return result
        else:
            # Task not found for this user
            print(f"[MCP] Could not find task {task_id} for user {user_id}")
            return {
                "task_id": task_id,
                "status": "not_found",
                "title": "Task not found"
            }


def update_task(user_id: str, task_id: int, title: Optional[str] = None, description: Optional[str] = None) -> Dict[str, Any]:
    """
    Modify an existing task
    """
    # Get a database session and update the task
    with next(get_session()) as session:
        # Find the task for the specific user
        task = session.exec(
            select(Task).where(Task.id == task_id, Task.user_id == user_id)
        ).first()

        if task:
            # Update the fields if provided
            if title is not None:
                task.title = title
            if description is not None:
                task.description = description

            session.add(task)
            session.commit()
            session.refresh(task)

            result = {
                "task_id": task.id,
                "status": "updated",
                "title": task.title,
                "description": task.description
            }

            print(f"[MCP] Updated task {task.id} for user {user_id}")
            return result
        else:
            # Task not found for this user
            print(f"[MCP] Could not find task {task_id} for user {user_id}")
            return {
                "task_id": task_id,
                "status": "not_found",
                "title": "Task not found"
            }


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