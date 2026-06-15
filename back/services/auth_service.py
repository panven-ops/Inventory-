from repositories.repo_users import get_user_by_username, create_user, update_user
from auth import verify_password, hash_password, create_access_token, create_refresh_token
from fastapi import HTTPException
from datetime import datetime, timedelta, timezone
from sqlalchemy.exc import IntegrityError

MAX_ATTEMPTS = 5
LOCK_TIME = 5  # minutes


def register_user(db, user):
    hashed = hash_password(user.password)
    try:
        return create_user(db, user.username, hashed)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Username already exists")


def login_user(db, user):
    db_user = get_user_by_username(db, user.username)

    if not db_user:
        raise HTTPException(status_code=401, detail="Wrong credentials")

    if db_user.lock_until and db_user.lock_until > datetime.now(timezone.utc):
        raise HTTPException(status_code=403, detail="Account locked")

    if not verify_password(user.password, db_user.password):
        db_user.failed_attempts += 1

        if db_user.failed_attempts >= MAX_ATTEMPTS:
            db_user.lock_until = datetime.now(timezone.utc) + timedelta(minutes=LOCK_TIME)
            db_user.failed_attempts = 0

        update_user(db, db_user)
        raise HTTPException(status_code=401, detail="Wrong credentials")

    db_user.failed_attempts = 0
    db_user.lock_until = None
    update_user(db, db_user)

    access = create_access_token({"user_id": db_user.id})
    refresh = create_refresh_token({"user_id": db_user.id})

    return access, refresh
