from sqlalchemy.orm import Session
from db_models import LogDB

def create_log(db: Session, action: str, user_id: int = None,
               ip_address: str = None, endpoint: str = None,
               status_code: int = None, details: str = None):
    log = LogDB(
        action=action,
        user_id=user_id,
        ip_address=ip_address,
        endpoint=endpoint,
        status_code=status_code,
        details=details
    )
    db.add(log)
    db.commit()
    return log

def get_logs_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 50):
    return (
        db.query(LogDB)
        .filter(LogDB.user_id == user_id)
        .order_by(LogDB.timestamp.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )

def get_all_logs(db: Session, skip: int = 0, limit: int = 100):
    return (
        db.query(LogDB)
        .order_by(LogDB.timestamp.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )

def get_security_logs(db: Session, skip: int = 0, limit: int = 100):
    security_actions = ["FAILED_LOGIN", "UNAUTHORIZED_ACCESS", "RATE_LIMIT_EXCEEDED"]
    return (
        db.query(LogDB)
        .filter(LogDB.action.in_(security_actions))
        .order_by(LogDB.timestamp.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
