from sqlalchemy.orm import Session
from db_models import UserDB

def get_user_by_username(db: Session, username: str):
    return db.query(UserDB).filter(UserDB.username == username).first()

def create_user(db: Session, username: str, password: str):
    user = UserDB(username=username, password=password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def update_user(db: Session, user: UserDB):
    db.commit()
    db.refresh(user)
    return user

def get_user_by_id(db: Session, user_id: int):
    return db.query(UserDB).filter(UserDB.id == user_id).first()
