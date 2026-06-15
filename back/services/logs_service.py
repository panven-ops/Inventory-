from repositories.repo_logs import (
    create_log,
    get_logs_by_user,
    get_all_logs,
    get_security_logs
)

# WRITE LOG
def write_log(db, action: str, user_id: int = None,
              ip_address: str = None, endpoint: str = None,
              status_code: int = None, details: str = None):
    return create_log(
        db=db,
        action=action,
        user_id=user_id,
        ip_address=ip_address,
        endpoint=endpoint,
        status_code=status_code,
        details=details
    )

# GET MY LOGS
def get_my_logs(db, user_id: int, skip: int = 0, limit: int = 50):
    logs = get_logs_by_user(db, user_id, skip, limit)
    return [log.to_dict() for log in logs]

def get_all_logs_service(db, skip: int = 0, limit: int = 100):
    logs = get_all_logs(db, skip, limit)
    return [log.to_dict() for log in logs]

def get_security_logs_service(db, skip: int = 0, limit: int = 100):
    logs = get_security_logs(db, skip, limit)
    return [log.to_dict() for log in logs]
