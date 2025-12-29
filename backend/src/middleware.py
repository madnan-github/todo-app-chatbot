"""Rate limiting middleware for API endpoints."""
import time
from typing import Dict, Tuple
from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse


class RateLimiter:
    """Simple in-memory rate limiter using sliding window algorithm."""

    def __init__(self, max_requests: int = 100, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.clients: Dict[str, list[float]] = {}

    def _get_client_key(self, request: Request) -> str:
        """Get unique client identifier from request."""
        # Use X-Forwarded-For for proxied requests, fallback to client host
        forwarded = request.headers.get("X-Forwarded-For")
        if forwarded:
            return forwarded.split(",")[0].strip()
        return request.client.host if request.client else "unknown"

    def _cleanup_old_requests(self, client_key: str, current_time: float) -> None:
        """Remove requests outside the current window."""
        if client_key in self.clients:
            self.clients[client_key] = [
                ts for ts in self.clients[client_key]
                if current_time - ts < self.window_seconds
            ]

    def is_rate_limited(self, request: Request) -> Tuple[bool, int, int]:
        """
        Check if request is rate limited.
        Returns (is_limited, remaining_requests, reset_time_seconds).
        """
        client_key = self._get_client_key(request)
        current_time = time.time()

        # Cleanup old entries
        self._cleanup_old_requests(client_key, current_time)

        # Get or initialize client requests
        if client_key not in self.clients:
            self.clients[client_key] = []

        request_count = len(self.clients[client_key])

        if request_count >= self.max_requests:
            # Calculate reset time
            oldest_request = min(self.clients[client_key])
            reset_time = int(oldest_request + self.window_seconds - current_time)
            return True, 0, max(0, reset_time)

        # Record this request
        self.clients[client_key].append(current_time)
        remaining = self.max_requests - len(self.clients[client_key])
        return False, remaining, self.window_seconds


# Global rate limiter instance
rate_limiter = RateLimiter(max_requests=100, window_seconds=60)


async def rate_limit_dependency(request: Request) -> None:
    """
    FastAPI dependency for rate limiting.
    Use: @app.get("/endpoint", dependencies=[Depends(rate_limit_dependency)])
    """
    is_limited, remaining, reset_time = rate_limiter.is_rate_limited(request)

    if is_limited:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail={
                "error": "Rate limit exceeded",
                "message": f"Too many requests. Please wait {reset_time} seconds.",
                "retry_after": reset_time,
            },
            headers={"Retry-After": str(reset_time)},
        )
