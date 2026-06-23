import redis.asyncio as aioredis
import os

redis_client = aioredis.Redis(
    host=os.getenv("REDIS_HOST"),
    port=int(os.getenv("REDIS_PORT", 6379)),
    decode_responses=True
)

async def get_redis() -> aioredis.Redis:

    return redis_client
