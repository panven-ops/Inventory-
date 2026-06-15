from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from jose import jwt, JWTError
from database import SessionLocal
from services.logs_service import write_log
import os

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"

# =========================
# HELPER - Διαβάζει το token
# =========================
def get_user_id_from_request(request: Request):
    # Παίρνει το Authorization header
    auth = request.headers.get("Authorization")
    if not auth or not auth.startswith("Bearer "):
        return None
    token = auth.split(" ")[1]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("user_id")
    except JWTError:
        return None

# =========================
# HELPER - Αποφασίζει action
# =========================
def get_action(method: str, path: str, status_code: int):
    # Login / Register
    if path == "/login":
        return "LOGIN" if status_code == 200 else "FAILED_LOGIN"
    if path == "/register":
        return "REGISTER" if status_code == 200 else "FAILED_REGISTER"

    # Rate limit - ανεξάρτητα από endpoint
    if status_code == 429:
        return "RATE_LIMIT_EXCEEDED"

    # Unauthorized
    if status_code == 403:
        return "UNAUTHORIZED_ACCESS"

    # Items
    if path.startswith("/items"):
        if method == "POST":
            return "CREATE_ITEM"
        if method == "DELETE":
            return "DELETE_ITEM"
        if method == "PUT":
            return "UPDATE_ITEM"
        if method == "GET":
            return "GET_ITEMS"

    return "OTHER"

# =========================
# MIDDLEWARE
# =========================
class LogMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # 1. Παίρνουμε πληροφορίες από το request
        ip = request.client.host
        path = request.url.path
        method = request.method
        user_id = get_user_id_from_request(request)

        # 2. Αφήνουμε το request να περάσει στο endpoint
        response = await call_next(request)
        status_code = response.status_code

        # 3. Δεν γράφουμε log για τα /logs endpoints
        # (αλλιώς κάθε φορά που βλέπεις logs, δημιουργείται νέο log!)
        if path.startswith("/logs"):
            return response

        # 4. Αποφασίζουμε τι action είναι
        action = get_action(method, path, status_code)

        # 5. Γράφουμε το log στη DB
        db = SessionLocal()
        try:
            write_log(
                db=db,
                action=action,
                user_id=user_id,
                ip_address=ip,
                endpoint=f"{method} {path}",
                status_code=status_code
            )
        finally:
            db.close()

        return response
