import asyncio
from src.database import init_db
from src.models import User, Task, Tag, TaskTag
from src.auth import hash_password
from sqlmodel import select
from src.database import async_session_maker

async def verify():
    print("--- Starting Verification Script ---")
    await init_db()
    
    async with async_session_maker() as session:
        # 1. Setup - Create two users for isolation test
        user_a_id = "user_a_123"
        user_b_id = "user_b_456"
        
        # Clean up if exists
        for uid in [user_a_id, user_b_id]:
            result = await session.execute(select(User).where(User.id == uid))
            u = result.scalar_one_or_none()
            if u: await session.delete(u)
        await session.commit()
        
        user_a = User(id=user_a_id, email="a@example.com", password_hash=hash_password("password123"))
        user_b = User(id=user_b_id, email="b@example.com", password_hash=hash_password("password123"))
        session.add(user_a)
        session.add(user_b)
        await session.commit()
        print("Users created.")

        # 2. Tag CRUD Verification
        tag_name = "urgent"
        tag_a = Tag(user_id=user_a_id, name=tag_name)
        session.add(tag_a)
        await session.commit()
        await session.refresh(tag_a)
        print(f"Tag created: {tag_a.name} (ID: {tag_a.id})")
        
        # Verify listing tags
        result = await session.execute(select(Tag).where(Tag.user_id == user_a_id))
        tags = result.scalars().all()
        assert any(t.name == tag_name for t in tags), "Tag listing failed"
        print("Tag listing verified.")

        # 3. Search & Filter Verification
        task1 = Task(user_id=user_a_id, title="Buy milk", description="Grocery shopping", priority="high")
        task2 = Task(user_id=user_a_id, title="Fix bug", description="API error", priority="low", completed=True)
        session.add(task1)
        session.add(task2)
        await session.commit()
        await session.refresh(task1)
        await session.refresh(task2)
        
        # Associate tag
        task_tag = TaskTag(task_id=task1.id, tag_id=tag_a.id)
        session.add(task_tag)
        await session.commit()
        print("Tasks created and tag associated.")

        # Verify priority filter
        result = await session.execute(select(Task).where(Task.user_id == user_a_id, Task.priority == "high"))
        high_tasks = result.scalars().all()
        assert len(high_tasks) == 1 and high_tasks[0].title == "Buy milk", "Priority filter failed"
        print("Priority filter verified.")

        # Verify search filter (ILIKE)
        search_term = "%MILK%"
        result = await session.execute(select(Task).where(Task.user_id == user_a_id, Task.title.ilike(search_term)))
        search_tasks = result.scalars().all()
        assert len(search_tasks) == 1, "Search filter (ILIKE) failed"
        print("Search filter (ILIKE) verified.")

        # Verify tag filter
        result = await session.execute(select(Task).join(TaskTag).where(Task.user_id == user_a_id, TaskTag.tag_id == tag_a.id))
        tagged_tasks = result.scalars().all()
        assert len(tagged_tasks) == 1 and tagged_tasks[0].title == "Buy milk", "Tag filter failed"
        print("Tag filter verified.")

        # 4. User Isolation Verification
        # User B should not see User A tasks
        result = await session.execute(select(Task).where(Task.user_id == user_b_id))
        b_tasks = result.scalars().all()
        assert len(b_tasks) == 0, "User isolation failed: User B sees User A tasks"
        print("User isolation verified.")

        # Cleanup
        await session.delete(task1)
        await session.delete(task2)
        await session.delete(tag_a)
        await session.delete(user_a)
        await session.delete(user_b)
        await session.commit()
        print("Cleanup completed.")
        print("--- All verifications passed ---")

if __name__ == "__main__":
    asyncio.run(verify())
