#!/usr/bin/env python3
"""
Comprehensive test to verify all MCP functions work properly.
"""

import uuid
from app.mcp_server import add_task, list_tasks, complete_task, delete_task, update_task
from app.database import create_db_and_tables
from src.models import User
from sqlmodel import select
from app.database import get_session

def comprehensive_test():
    """Comprehensive test of all MCP functions"""
    print("Creating database tables...")
    create_db_and_tables()

    # Use a unique user ID for this test
    test_user_id = f"comprehensive-test-user-{uuid.uuid4()}"

    # Create a test user
    with next(get_session()) as session:
        test_user = User(
            id=test_user_id,
            email=f"ctest_{uuid.uuid4()}@example.com",
            password_hash="$2b$12$dummy_hash_for_testing_purposes_only",
            name="Comprehensive Test User"
        )
        session.add(test_user)
        session.commit()
        print(f"Created test user: {test_user_id}")

    print("\n=== COMPREHENSIVE MCP FUNCTION TEST ===")

    # Test 1: Add task
    print("\n1. Testing ADD_TASK function...")
    try:
        task_result = add_task(test_user_id, "Comprehensive Test Task", "This is a test for comprehensive functionality")
        print(f"   ✓ ADD_TASK successful: {task_result}")
        task_id = task_result["task_id"]
    except Exception as e:
        print(f"   ❌ ADD_TASK failed: {str(e)}")
        return

    # Test 2: List tasks
    print("\n2. Testing LIST_TASKS function...")
    try:
        tasks = list_tasks(test_user_id)
        print(f"   ✓ LIST_TASKS successful: Found {len(tasks)} tasks")
        for task in tasks:
            print(f"     - ID: {task['id']}, Title: {task['title']}, Completed: {task['completed']}")
    except Exception as e:
        print(f"   ❌ LIST_TASKS failed: {str(e)}")

    # Test 3: Update task
    print("\n3. Testing UPDATE_TASK function...")
    try:
        update_result = update_task(test_user_id, task_id, "Updated Comprehensive Test Task", "Updated comprehensive test description")
        print(f"   ✓ UPDATE_TASK successful: {update_result}")
    except Exception as e:
        print(f"   ❌ UPDATE_TASK failed: {str(e)}")

    # Test 4: Complete task
    print("\n4. Testing COMPLETE_TASK function...")
    try:
        complete_result = complete_task(test_user_id, task_id)
        print(f"   ✓ COMPLETE_TASK successful: {complete_result}")
    except Exception as e:
        print(f"   ❌ COMPLETE_TASK failed: {str(e)}")

    # Test 5: List tasks again to see completion
    print("\n5. Testing LIST_TASKS to verify completion...")
    try:
        completed_tasks = list_tasks(test_user_id, "completed")
        print(f"   ✓ LIST_TASKS (completed) successful: Found {len(completed_tasks)} completed tasks")
        for task in completed_tasks:
            print(f"     - ID: {task['id']}, Title: {task['title']}, Completed: {task['completed']}")
    except Exception as e:
        print(f"   ❌ LIST_TASKS (completed) failed: {str(e)}")

    # Test 6: Delete task
    print("\n6. Testing DELETE_TASK function...")
    try:
        delete_result = delete_task(test_user_id, task_id)
        print(f"   ✓ DELETE_TASK successful: {delete_result}")
    except Exception as e:
        print(f"   ❌ DELETE_TASK failed: {str(e)}")

    # Test 7: List tasks to verify deletion
    print("\n7. Testing LIST_TASKS to verify deletion...")
    try:
        remaining_tasks = list_tasks(test_user_id)
        print(f"   ✓ LIST_TASKS (after deletion) successful: Found {len(remaining_tasks)} remaining tasks")
    except Exception as e:
        print(f"   ❌ LIST_TASKS (after deletion) failed: {str(e)}")

    print("\n=== TEST SUMMARY ===")
    print("If all tests showed ✓, then all MCP functions are working properly!")
    print("The AI chatbot should now properly handle all task operations.")

if __name__ == "__main__":
    comprehensive_test()