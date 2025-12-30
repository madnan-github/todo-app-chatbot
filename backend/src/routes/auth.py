"""Authentication routes."""
import uuid
from fastapi import APIRouter, HTTPException, status, Depends, Response, Request
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.auth import create_access_token, get_current_user, hash_password, verify_password, verify_token
from src.config import settings
from src.database import get_session
from src.models import User
from src.schemas import UserCreate, UserLogin, UserResponse, BetterAuthResponse, BetterAuthUser, SessionInfo
from datetime import datetime, timedelta

router = APIRouter(prefix="/api/v1/auth", tags=["Authentication"])


@router.post("/signup", response_model=BetterAuthResponse, status_code=status.HTTP_201_CREATED)
async def signup(
    user_data: UserCreate,
    response: Response,
    session: AsyncSession = Depends(get_session),
):
    """Register a new user."""
    # Check if email already exists
    result = await session.execute(
        select(User).where(User.email == user_data.email.lower())
    )
    existing_user = result.scalar_one_or_none()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered",
        )

    # Create new user
    hashed_password = hash_password(user_data.password)
    new_user = User(
        id=str(uuid.uuid4()),
        email=user_data.email.lower(),
        password_hash=hashed_password,
        name=user_data.name,
    )
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)

    # Create JWT token
    expires_delta = timedelta(minutes=settings.jwt_expiration_minutes)
    expires_at = datetime.utcnow() + expires_delta
    access_token = create_access_token(user_id=new_user.id, email=new_user.email, expires_delta=expires_delta)

    # Set session cookie
    response.set_cookie(
        key="session_token",
        value=access_token,
        httponly=True,
        secure=settings.environment == "production",
        samesite="lax",
        max_age=60 * 60 * 24 * 7,  # 7 days
    )

    return BetterAuthResponse(
        user=BetterAuthUser(id=new_user.id, email=new_user.email, name=new_user.name),
        session=SessionInfo(token=access_token, expiresAt=expires_at)
    )


@router.post("/signin", response_model=BetterAuthResponse)
async def signin(
    credentials: UserLogin,
    response: Response,
    session: AsyncSession = Depends(get_session),
):
    """Authenticate user and return JWT token."""
    # Find user by email
    result = await session.execute(
        select(User).where(User.email == credentials.email.lower())
    )
    user = result.scalar_one_or_none()

    if user is None or not verify_password(credentials.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    # Create JWT token
    expires_delta = timedelta(minutes=settings.jwt_expiration_minutes)
    expires_at = datetime.utcnow() + expires_delta
    access_token = create_access_token(user_id=user.id, email=user.email, expires_delta=expires_delta)

    # Set session cookie
    response.set_cookie(
        key="session_token",
        value=access_token,
        httponly=True,
        secure=settings.environment == "production",
        samesite="lax",
        max_age=60 * 60 * 24 * 7,  # 7 days
    )

    return BetterAuthResponse(
        user=BetterAuthUser(id=user.id, email=user.email, name=user.name),
        session=SessionInfo(token=access_token, expiresAt=expires_at)
    )


@router.post("/signout")
async def signout(response: Response):
    """Sign out user by clearing the session cookie."""
    response.delete_cookie(
        key="session_token",
        httponly=True,
        secure=settings.environment == "production",
        samesite="lax",
    )
    return {"success": True}


@router.get("/session", response_model=BetterAuthResponse)
async def get_session_info(
    request: Request,
    session_db: AsyncSession = Depends(get_session)
):
    """Get current session info from cookie."""
    token = request.cookies.get("session_token")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )

    payload = verify_token(token)
    user_id = payload.get("sub")
    expires_at = datetime.fromtimestamp(payload.get("exp"))

    result = await session_db.execute(
        select(User).where(User.id == user_id)
    )
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )

    return BetterAuthResponse(
        user=BetterAuthUser(id=user.id, email=user.email, name=user.name),
        session=SessionInfo(token=token, expiresAt=expires_at)
    )


@router.get("/me", response_model=UserResponse)
async def get_me(
    current_user: UserResponse = Depends(get_current_user),
):
    """Get current authenticated user."""
    return current_user
