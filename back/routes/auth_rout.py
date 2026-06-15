from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from database import get_db
from model import UserLogin, UserCreate
from services.auth_service import register_user, login_user
from auth import get_refresh_user, create_access_token
from lim import limiter

router = APIRouter()


@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    register_user(db, user)
    return {"message": "User Created"}


@router.post("/login")
@limiter.limit("5/minute")
def login(request: Request, user: UserLogin, db: Session = Depends(get_db)):
    access, refresh = login_user(db, user)

    return {
        "access_token": access,
        "refresh_token": refresh,
        "token_type": "bearer"
    }


@router.post("/refresh")
def refresh(user_id: int = Depends(get_refresh_user)):
    return {
        "access_token": create_access_token({"user_id": user_id}),
        "token_type": "bearer"
    }
