from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from database import get_db
from auth import get_current_user, get_current_admin
from services.logs_service import get_my_logs, get_all_logs_service, get_security_logs_service

router = APIRouter()

# GET MY ACTIVITY
@router.get("/logs/me")
def my_logs(user_id: int = Depends(get_current_user), db: Session = Depends(get_db), skip: int = Query(0, ge=0), limit: int = Query(50, ge=1, le=100)):
    return get_my_logs(db, user_id, skip, limit)


# GET ALL LOGS (μόνο admin)
@router.get("/logs/all")
def all_logs(user_id: int = Depends(get_current_admin), db: Session = Depends(get_db), skip: int = Query(0, ge=0), limit: int = Query(100, ge=1, le=500)):

    return get_all_logs_service(db, skip, limit)


# GET SECUR LOGS (admin only)
@router.get("/logs/security")
def security_logs(user_id: int = Depends(get_current_admin), db: Session = Depends(get_db), skip: int = Query(0, ge=0), limit: int = Query(100, ge=1, le=500)):

    return get_security_logs_service(db, skip, limit)
