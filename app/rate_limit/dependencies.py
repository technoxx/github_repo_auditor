from fastapi import Depends, HTTPException, status
from app.auth.dependencies import get_current_user
from app.db.models import User
from app.rate_limit.limiter import RateLimiter

# 10 audits per hour per user
limiter = RateLimiter(limit=2, window_seconds=3600)

def audit_rate_limit(user:User = Depends(get_current_user)):
    key = f"user:{user.id}"
    if not limiter.allow(key):
        raise HTTPException(
        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
        detail="Rate limit exceeded. Try again later."
        )
    return user