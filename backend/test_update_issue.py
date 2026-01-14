#!/usr/bin/env python3
"""
Test script to reproduce the update task issue.
"""

import uuid
from app.mcp_server import add_task, list_tasks, complete_task, delete_task, update_task
from app.database import create_db_and_tables
from src.models import User
from sqlmodel import select
from app.database import get_session

def test_update_issue():
    """Test the specific update issue"""
    print("Creating database tables...")
    create_db_and_tables()

    # Use a unique user ID for this test
    test_user_id = f"update-test-user-{uuid.uuid4()}"

    # Create a test user
    with next(get_session()) as session:
        test_user = User(
            id=test_user_id,
            email=f"update_test_{uuid.uuid4()}@example.com",
            password_hash="$2b$12$dummy_hash_for_testing_purposes_only",
            name="Update Test User"
        )
        session.add(test_user)
        session.commit()
        print(f"Created test user: {test_user_id}")

    print("\n=== TESTING UPDATE ISSUE ===")

    # 1. Add a task first
    print("\n1. Adding a test task...")
    try:
        add_result = add_task(test_user_id, "but system", "Initial description")
        print(f"   ✓ Task created: ID {add_result['task_id']}")
        task_id = add_result["task_id"]
    except Exception as e:
        print(f"   ❌ ADD failed: {e}")
        return

    # 2. Verify the task exists
    print("\n2. Verifying task exists...")
    try:
        tasks = list_tasks(test_user_id)
        print(f"   ✓ Found {len(tasks)} tasks")
        for task in tasks:
            print(f"     - ID: {task['id']}, Title: '{task['title']}', Description: '{task['description']}'")
    except Exception as e:
        print(f"   ❌ LIST failed: {e}")

    # 3. Try to update the task (this is the problematic operation)
    print(f"\n3. Updating task {task_id} from 'but system' to 'buy Laptop System'...")
    try:
        update_result = update_task(test_user_id, task_id, "buy Laptop System", "Updated description")
        print(f"   ✓ Update result: {update_result}")

        # Check if the update was actually applied
        updated_tasks = list_tasks(test_user_id)
        print(f"   ✓ After update - Found {len(updated_tasks)} tasks")
        for task in updated_tasks:
            print(f"     - ID: {task['id']}, Title: '{task['title']}', Description: '{task['description']}'")

        # Verify the specific task was updated
        target_task = next((t for t in updated_tasks if t['id'] == task_id), None)
        if target_task:
            if target_task['title'] == 'buy Laptop System':
                print(f"   ✓ Task {task_id} was successfully updated to 'buy Laptop System'")
            else:
                print(f"   ❌ Task {task_id} was NOT updated. Still '{target_task['title']}' instead of 'buy Laptop System'")
        else:
            print(f"   ❌ Task {task_id} not found after update")

    except Exception as e:
        print(f"   ❌ UPDATE failed: {e}")

    # 4. Clean up
    print(f"\n4. Cleaning up...")
    try:
        delete_result = delete_task(test_user_id, task_id)
        print(f"   ✓ Task {task_id} deleted")
    except Exception as e:
        print(f"   ❌ DELETE failed: {e}")

    print("\n=== TEST COMPLETE ===")

if __name__ == "__main__":
    test_update_issue()