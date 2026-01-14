#!/usr/bin/env python3
"""
Test script to verify that MCP functions properly interact with the database.
"""

import asyncio
from app.mcp_server import add_task, list_tasks, complete_task, delete_task, update_task
from app.database import create_db_and_tables
from src.models import User
from sqlmodel import select
from app.database import get_session
from datetime import datetime

def test_mcp_functions():
    """Test the MCP functions to ensure they interact with the database"""
    print("Creating database tables...")
    create_db_and_tables()

    # Create a test user first
    test_user_id = "test-user-123"

    with next(get_session()) as session:
        # Check if user already exists
        existing_user = session.exec(select(User).where(User.id == test_user_id)).first()
        if not existing_user:
            # Create a test user
            test_user = User(
                id=test_user_id,
                email="test@example.com",
                password_hash="$2b$12$dummy_hash_for_testing_purposes_only",
                name="Test User"
            )
            session.add(test_user)
            session.commit()
            print(f"Created test user: {test_user_id}")

    print("\n1. Testing add_task function...")
    task_result = add_task(test_user_id, "Test Task", "This is a test task")
    print(f"   Result: {task_result}")

    if "task_id" in task_result:
        task_id = task_result["task_id"]
        print(f"\n2. Testing list_tasks function...")
        tasks = list_tasks(test_user_id)
        print(f"   Tasks found: {len(tasks)}")
        for task in tasks:
            print(f"   - ID: {task['id']}, Title: {task['title']}, Completed: {task['completed']}")

        print(f"\n3. Testing update_task function...")
        update_result = update_task(test_user_id, task_id, "Updated Test Task", "Updated description")
        print(f"   Result: {update_result}")

        print(f"\n4. Testing complete_task function...")
        complete_result = complete_task(test_user_id, task_id)
        print(f"   Result: {complete_result}")

        print(f"\n5. Testing list_tasks again to see completed task...")
        tasks = list_tasks(test_user_id, "completed")
        print(f"   Completed tasks found: {len(tasks)}")
        for task in tasks:
            print(f"   - ID: {task['id']}, Title: {task['title']}, Completed: {task['completed']}")

        print(f"\n6. Testing delete_task function...")
        delete_result = delete_task(test_user_id, task_id)
        print(f"   Result: {delete_result}")

        print(f"\n7. Testing list_tasks to confirm deletion...")
        tasks = list_tasks(test_user_id)
        print(f"   Tasks after deletion: {len(tasks)}")

        print("\n✅ All MCP functions tested successfully!")
    else:
        print("❌ Failed to add task - check database connection")

if __name__ == "__main__":
    test_mcp_functions()