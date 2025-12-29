"""Better Auth compatible API routes.

These endpoints mirror Better Auth's API structure so the frontend
can use Better Auth client with our custom FastAPI backend.
"""
import bcrypt
import uuid
from datetime import datetime, timedelta
from typing import Optional
from fastapi import APIRouter, HTTPException, status, Depends, Response, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.auth import create_access_token, decode_access_token
from src.database import get_session
from src.models import User
from src.config import settings

# Better Auth client uses /api/auth as its base path by default
# We create routers for both /api/auth and /api/v1 to support different configurations
router = APIRouter(prefix="/api/auth", tags=["Better Auth"])
router_v1 = APIRouter(prefix="/api/v1", tags=["Better Auth V1"])


def hash_password(password: str) -> str:
    """Hash a password using bcrypt."""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


def verify_password(password: str, hashed: str) -> bool:
    """Verify a password against a bcrypt hash."""
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))


# Request/Response models for Better Auth compatibility
class SignUpEmailRequest(BaseModel):
    """Sign up with email request body."""
    name: str
    email: EmailStr
    password: str
    image: Optional[str] = None
    callbackURL: Optional[str] = None


class SignInEmailRequest(BaseModel):
    """Sign in with email request body."""
    email: EmailStr
    password: str
    callbackURL: Optional[str] = None
    rememberMe: Optional[bool] = True


class BetterAuthUser(BaseModel):
    """Better Auth user response format."""
    id: str
    name: str
    email: str
    emailVerified: bool = True
    image: Optional[str] = None
    createdAt: str
    updatedAt: str


class BetterAuthSession(BaseModel):
    """Better Auth session response format."""
    id: str
    userId: str
    token: str
    expiresAt: str
    createdAt: str
    updatedAt: str


class SignUpResponse(BaseModel):
    """Sign up response."""
    user: BetterAuthUser
    session: BetterAuthSession


class SignInResponse(BaseModel):
    """Sign in response."""
    user: BetterAuthUser
    session: BetterAuthSession


class SessionResponse(BaseModel):
    """Get session response."""
    user: BetterAuthUser
    session: BetterAuthSession


def create_session_response(user: User, token: str) -> dict:
    """Create a Better Auth compatible session response."""
    now = datetime.utcnow().isoformat() + "Z"
    expires_at = datetime.utcnow() + timedelta(days=7)  # 7 days expiration

    return {
        "user": {
            "id": user.id,
            "name": user.name or "",
            "email": user.email,
            "emailVerified": True,
            "image": None,
            "createdAt": user.created_at.isoformat() + "Z" if user.created_at else now,
            "updatedAt": now,
        },
        "session": {
            "id": str(uuid.uuid4()),
            "userId": user.id,
            "token": token,
            "expiresAt": expires_at.isoformat() + "Z",
            "createdAt": now,
            "updatedAt": now,
        }
    }


@router.post("/sign-up/email")
async def sign_up_email(
    request: SignUpEmailRequest,
    response: Response,
    session: AsyncSession = Depends(get_session),
):
    """Sign up with email - Better Auth compatible endpoint."""
    # Check if email already exists
    result = await session.execute(
        select(User).where(User.email == request.email.lower())
    )
    existing_user = result.scalar_one_or_none()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered",
        )

    # Create new user
    hashed_password = hash_password(request.password)
    new_user = User(
        id=str(uuid.uuid4()),
        email=request.email.lower(),
        password_hash=hashed_password,
        name=request.name,
    )
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)

    # Create JWT token
    access_token = create_access_token(user_id=new_user.id, email=new_user.email)

    # Set session cookie (Better Auth style)
    response.set_cookie(
        key="better-auth.session_token",
        value=access_token,
        httponly=True,
        secure=settings.environment == "production",
        samesite="lax",
        max_age=60 * 60 * 24 * 7,  # 7 days
    )

    return create_session_response(new_user, access_token)


@router.post("/sign-in/email")
async def sign_in_email(
    request: SignInEmailRequest,
    response: Response,
    session: AsyncSession = Depends(get_session),
):
    """Sign in with email - Better Auth compatible endpoint."""
    # Find user by email
    result = await session.execute(
        select(User).where(User.email == request.email.lower())
    )
    user = result.scalar_one_or_none()

    if user is None or not verify_password(request.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    # Create JWT token
    access_token = create_access_token(user_id=user.id, email=user.email)

    # Set session cookie (Better Auth style)
    response.set_cookie(
        key="better-auth.session_token",
        value=access_token,
        httponly=True,
        secure=settings.environment == "production",
        samesite="lax",
        max_age=60 * 60 * 24 * 7,  # 7 days
    )

    return create_session_response(user, access_token)


@router.post("/sign-out")
async def sign_out(response: Response):
    """Sign out - Better Auth compatible endpoint."""
    response.delete_cookie(
        key="better-auth.session_token",
        httponly=True,
        secure=settings.environment == "production",
        samesite="lax",
    )
    return {"success": True}


async def _get_session_logic(request: Request, db_session: AsyncSession):
    """Shared logic for getting session - used by both /session and /get-session."""
    # Get token from cookie or Authorization header
    token = request.cookies.get("better-auth.session_token")

    if not token:
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header[7:]

    if not token:
        return JSONResponse(
            status_code=200,
            content=None,
        )

    try:
        payload = decode_access_token(token)
        user_id = payload.get("sub") or payload.get("user_id")

        if not user_id:
            return JSONResponse(status_code=200, content=None)

        # Get user from database
        result = await db_session.execute(
            select(User).where(User.id == user_id)
        )
        user = result.scalar_one_or_none()

        if not user:
            return JSONResponse(status_code=200, content=None)

        return create_session_response(user, token)
    except Exception:
        return JSONResponse(status_code=200, content=None)


@router.get("/get-session")
async def get_session_better_auth(
    request: Request,
    session: AsyncSession = Depends(get_session),
):
    """Get current session - Better Auth compatible endpoint (alternate path)."""
    return await _get_session_logic(request, session)


@router.get("/session")
async def get_session_endpoint(
    request: Request,
    session: AsyncSession = Depends(get_session),
):
    """Get current session - Better Auth compatible endpoint."""
    return await _get_session_logic(request, session)


# =====================================================
# V1 Router - Duplicate endpoints for /api/v1/* paths
# Better Auth client may use different base paths
# =====================================================

@router_v1.post("/sign-up/email")
async def sign_up_email_v1(
    request: SignUpEmailRequest,
    response: Response,
    session: AsyncSession = Depends(get_session),
):
    """Sign up with email - Better Auth compatible endpoint (v1)."""
    result = await session.execute(
        select(User).where(User.email == request.email.lower())
    )
    existing_user = result.scalar_one_or_none()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered",
        )

    hashed_password = hash_password(request.password)
    new_user = User(
        id=str(uuid.uuid4()),
        email=request.email.lower(),
        password_hash=hashed_password,
        name=request.name,
    )
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)

    access_token = create_access_token(user_id=new_user.id, email=new_user.email)

    response.set_cookie(
        key="better-auth.session_token",
        value=access_token,
        httponly=True,
        secure=settings.environment == "production",
        samesite="lax",
        max_age=60 * 60 * 24 * 7,
    )

    return create_session_response(new_user, access_token)


@router_v1.post("/sign-in/email")
async def sign_in_email_v1(
    request: SignInEmailRequest,
    response: Response,
    session: AsyncSession = Depends(get_session),
):
    """Sign in with email - Better Auth compatible endpoint (v1)."""
    result = await session.execute(
        select(User).where(User.email == request.email.lower())
    )
    user = result.scalar_one_or_none()

    if user is None or not verify_password(request.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    access_token = create_access_token(user_id=user.id, email=user.email)

    response.set_cookie(
        key="better-auth.session_token",
        value=access_token,
        httponly=True,
        secure=settings.environment == "production",
        samesite="lax",
        max_age=60 * 60 * 24 * 7,
    )

    return create_session_response(user, access_token)


@router_v1.post("/sign-out")
async def sign_out_v1(response: Response):
    """Sign out - Better Auth compatible endpoint (v1)."""
    response.delete_cookie(
        key="better-auth.session_token",
        httponly=True,
        secure=settings.environment == "production",
        samesite="lax",
    )
    return {"success": True}


@router_v1.get("/get-session")
async def get_session_v1(
    request: Request,
    session: AsyncSession = Depends(get_session),
):
    """Get current session - Better Auth compatible endpoint (v1)."""
    return await _get_session_logic(request, session)


@router_v1.get("/session")
async def get_session_endpoint_v1(
    request: Request,
    session: AsyncSession = Depends(get_session),
):
    """Get current session - Better Auth compatible endpoint (v1)."""
    return await _get_session_logic(request, session)
