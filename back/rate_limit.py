from fastapi import Request, Depends, HTTPException
from redis.asyncio import Redis
import os
from jose import jwt, JWTError
from redis_client import get_redis
import re


SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"

class RateLimiter:

    def __init__(self, limit: int, window_seconds: int):
        self.limit = limit
        self.window_seconds = window_seconds


    async def __call__(self, request: Request, redis: Redis = Depends(get_redis)):
        identifier = self._get_identifier(request)
        normalized_path = re.sub(r'/\d+', '/{id}', request.url.path)
        key = f"rate:{identifier}:{normalized_path}"

        count = await redis.incr(key)

        if count == 1:
            await redis.expire(key, self.window_seconds)

        if count > self.limit:
            ttl = await redis.ttl(key)
            raise HTTPException(status_code = 429, detail = f"Rate limit has been reached. Retry after {ttl}s.")

    def _get_identifier(self, request: Request) -> str:
        auth = request.headers.get("Authorization")

        if not auth or not auth.startswith("Bearer"):
            return request.client.host

        try:
            token = auth.split(" ")[1]
            payload = jwt.decode(token, SECRET_KEY, algorithms = [ALGORITHM])
            user_id = payload.get("user_id")

            return str(user_id) if user_id else request.client.host

        except JWTError:
            return request.client.host


items_read_limiter    = RateLimiter(limit=30, window_seconds=60)
sub_items_read_limiter = RateLimiter(limit=30, window_seconds=60)

items_write_limiter   = RateLimiter(limit=10, window_seconds=60)

items_delete_limiter  = RateLimiter(limit=5, window_seconds=60)
