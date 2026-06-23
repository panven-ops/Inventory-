from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from database import get_db
from model import UserLogin, UserCreate
from services.auth_service import register_user, login_user
from auth import get_refresh_user, create_access_token
from rate_limit import RateLimiter

# Αυστηρά limits για auth endpoints
login_limiter    = RateLimiter(limit=5, window_seconds=60)
register_limiter = RateLimiter(limit=3, window_seconds=60)

router = APIRouter()

@router.post("/register")
async def register(
    request: Request,
    user: UserCreate,
    _: None = Depends(register_limiter),
    db: Session = Depends(get_db)
):
    register_user(db, user)
    return {"message": "User Created"}

@router.post("/login")
async def login(
    request: Request,
        user: UserLogin,
    _: None = Depends(login_limiter),
    db: Session = Depends(get_db)
):
    access, refresh = login_user(db, user)
    return {
        "access_token": access,
        "refresh_token": refresh,
        "token_type": "bearer"
    }

@router.post("/refresh")
async def refresh(user_id: int = Depends(get_refresh_user)):
    return {
        "access_token": create_access_token({"user_id": user_id}),
        "token_type": "bearer"
    }
