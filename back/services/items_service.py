import json
from fastapi import HTTPException
from sqlalchemy.orm import Session
from redis.asyncio import Redis
from repositories.repo_items import (get_items_by_user, get_item_by_id,create_item, delete_item, update_item, get_total_items)
from model import ItemOut

def items_list_key(user_id, skip, limit):
    return f"items:{user_id}:{skip}:{limit}"

def item_key(item_id):
    return f"item:{item_id}"

async def invalidate_user_cache(redis: Redis, user_id: int):
    async for key in redis.scan_iter(f"items:{user_id}:*"):
        await redis.delete(key)

async def get_user_items(db: Session, redis: Redis, user_id: int, skip: int, limit: int):
    cache_key = items_list_key(user_id, skip, limit)
    cached = await redis.get(cache_key)
    if cached:
        return json.loads(cached)

    items = get_items_by_user(db, user_id, skip, limit)
    total = get_total_items(db, user_id)
    result = {
        "data": [ItemOut.model_validate(i).model_dump() for i in items],
        "total": total,
        "skip": skip,
        "limit": limit,
        "pages": -(-total // limit)
    }
    await redis.setex(cache_key, 60, json.dumps(result))
    return result

async def get_single_item(db: Session, redis: Redis, item_id: int):
    cache_key = item_key(item_id)
    cached = await redis.get(cache_key)

    if cached:
        return json.loads(cached)

    item = get_item_by_id(db, item_id)

    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    data = ItemOut.model_validate(item).model_dump()
    await redis.setex(cache_key, 60, json.dumps(data))

    return data

async def add_item_service(db: Session, redis: Redis, item, user_id: int):

    new_item = create_item(db, item.name, user_id)
    await invalidate_user_cache(redis, user_id)

    return ItemOut.model_validate(new_item).model_dump()

async def delete_item_service(db: Session, redis: Redis, item_id: int, user_id: int):
    item = get_item_by_id(db, item_id)

    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    if item.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")

    delete_item(db, item)
    await redis.delete(item_key(item_id))
    await invalidate_user_cache(redis, user_id)

async def update_item_service(db: Session, redis: Redis, item_id: int, updated_item, user_id: int):
    item = get_item_by_id(db, item_id)

    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    if item.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")

    item.name = updated_item.name
    updated = update_item(db, item)
    await redis.delete(item_key(item_id))
    await invalidate_user_cache(redis, user_id)

    return ItemOut.model_validate(updated).model_dump()
