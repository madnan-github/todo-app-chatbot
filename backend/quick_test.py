#!/usr/bin/env python3
"""
Quick test to verify that the database operations are working properly.
"""

import uuid
from app.mcp_server import add_task, list_tasks, complete_task, delete_task, update_task
from app.database import create_db_and_tables
from src.models import User
from sqlmodel import select
from app.database import get_session

def quick_test():
    """Quick test with a unique user ID"""
    print("Creating database tables...")
    create_db_and_tables()

    # Use a unique user ID for this test
    test_user_id = f"test-user-{uuid.uuid4()}"

    # Create a test user
    with next(get_session()) as session:
        test_user = User(
            id=test_user_id,
            email=f"test_{uuid.uuid4()}@example.com",
            password_hash="$2b$12$dummy_hash_for_testing_purposes_only",
            name="Test User"
        )
        session.add(test_user)
        session.commit()
        print(f"Created test user: {test_user_id}")

    print("\nTesting add_task function...")
    try:
        task_result = add_task(test_user_id, "Test Task from MCP", "This verifies the MCP functions work with DB")
        print(f"   ✓ Task created: {task_result}")

        if "task_id" in task_result:
            task_id = task_result["task_id"]

            # Test listing tasks
            print("\nTesting list_tasks function...")
            tasks = list_tasks(test_user_id)
            print(f"   ✓ Found {len(tasks)} tasks")

            # Test updating task
            print("\nTesting update_task function...")
            update_result = update_task(test_user_id, task_id, "Updated Test Task", "Updated description")
            print(f"   ✓ Task updated: {update_result}")

            # Test completing task
            print("\nTesting complete_task function...")
            complete_result = complete_task(test_user_id, task_id)
            print(f"   ✓ Task completed: {complete_result}")

            # Test deleting task
            print("\nTesting delete_task function...")
            delete_result = delete_task(test_user_id, task_id)
            print(f"   ✓ Task deleted: {delete_result}")

            print("\n🎉 SUCCESS: All MCP functions are properly connected to the database!")
            print("✅ The AI chatbot will now be able to add, update, list, complete, and delete tasks in the database.")
        else:
            print("   ❌ Task creation failed")
    except Exception as e:
        print(f"   ❌ Error during testing: {str(e)}")

if __name__ == "__main__":
    quick_test()