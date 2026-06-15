import os
from slowapi import Limiter
from limiter import get_user_id_from_request

ENABLE_RATE_LIMIT = os.getenv("ENABLE_RATE_LIMIT", "true") == "true"

limiter = Limiter(
    key_func=get_user_id_from_request,
    enabled=ENABLE_RATE_LIMIT
)
