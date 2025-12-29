"""Tag management routes."""
from typing import Optional
from fastapi import APIRouter, HTTPException, status, Depends, Query
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from src.auth import get_user_id_from_token
from src.database import get_session
from src.models import User, Tag, TaskTag
from src.schemas import TagCreate, TagResponse, TagListResponse

router = APIRouter(prefix="/api/v1/tags", tags=["Tags"])


@router.get("", response_model=TagListResponse)
async def get_tags(
    user_id: str = Depends(get_user_id_from_token),
    session: AsyncSession = Depends(get_session),
    # Search for autocomplete
    search: Optional[str] = Query(None, min_length=1, max_length=50),
    # Pagination
    page: int = Query(1, ge=1),
    per_page: int = Query(50, ge=1, le=100),
):
    """Get user's tags with optional search filter for autocomplete."""
    # Build count query
    count_query = select(func.count(Tag.id)).where(Tag.user_id == user_id)

    # Build main query
    query = select(Tag).where(Tag.user_id == user_id)

    # Apply search filter for autocomplete
    if search:
        search_term = f"{search}%"
        query = query.where(Tag.name.ilike(search_term))
        count_query = count_query.where(Tag.name.ilike(search_term))

    # Get total count
    count_result = await session.execute(count_query)
    total = count_result.scalar()

    # Apply pagination
    offset = (page - 1) * per_page
    query = query.offset(offset).limit(per_page).order_by(Tag.name)

    # Execute query
    result = await session.execute(query)
    tags = result.scalars().all()

    return TagListResponse(
        tags=[TagResponse.model_validate(tag) for tag in tags],
        total=total,
        page=page,
        per_page=per_page,
    )


@router.get("/autocomplete")
async def get_tags_autocomplete(
    q: str = Query(..., min_length=1, max_length=50),
    user_id: str = Depends(get_user_id_from_token),
    session: AsyncSession = Depends(get_session),
    limit: int = Query(10, ge=1, le=20),
):
    """Get tag suggestions for autocomplete based on prefix search."""
    search_term = f"{q}%"
    query = (
        select(Tag.name)
        .where(Tag.user_id == user_id)
        .where(Tag.name.ilike(search_term))
        .order_by(Tag.name)
        .limit(limit)
    )

    result = await session.execute(query)
    tags = result.scalars().all()

    return {"suggestions": tags}


@router.post("", response_model=TagResponse, status_code=status.HTTP_201_CREATED)
async def create_tag(
    tag_data: TagCreate,
    user_id: str = Depends(get_user_id_from_token),
    session: AsyncSession = Depends(get_session),
):
    """Create a new tag for the user."""
    # Check if tag already exists for this user
    existing = await session.execute(
        select(Tag).where(Tag.user_id == user_id, Tag.name == tag_data.name.lower().strip())
    )
    if existing.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Tag with this name already exists",
        )

    # Create tag
    tag = Tag(
        user_id=user_id,
        name=tag_data.name.lower().strip(),
    )
    session.add(tag)
    await session.commit()
    await session.refresh(tag)

    return TagResponse.model_validate(tag)


@router.get("/{tag_id}", response_model=TagResponse)
async def get_tag(
    tag_id: int,
    user_id: str = Depends(get_user_id_from_token),
    session: AsyncSession = Depends(get_session),
):
    """Get a specific tag."""
    result = await session.execute(
        select(Tag).where(Tag.id == tag_id, Tag.user_id == user_id)
    )
    tag = result.scalar_one_or_none()

    if tag is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tag not found",
        )

    return TagResponse.model_validate(tag)


@router.delete("/{tag_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_tag(
    tag_id: int,
    user_id: str = Depends(get_user_id_from_token),
    session: AsyncSession = Depends(get_session),
):
    """Delete a tag."""
    result = await session.execute(
        select(Tag).where(Tag.id == tag_id, Tag.user_id == user_id)
    )
    tag = result.scalar_one_or_none()

    if tag is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tag not found",
        )

    await session.delete(tag)
    await session.commit()
