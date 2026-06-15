from fastapi import Request
from jose import jwt, JWTError
import os

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"

def get_user_id_from_request(request: Request):
    auth = request.headers.get("Authorization")

    if not auth or not auth.startswith("Bearer "):
        return request.client.host  # fallback to IP

    try:
        token = auth.split(" ")[1]
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        user_id = payload.get("user_id")

        if user_id is None:
            return request.client.host
        
        return str(user_id)
    
    except JWTError:
        return request.client.host
