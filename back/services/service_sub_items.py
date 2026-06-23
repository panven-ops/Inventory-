import json
from fastapi import HTTPException
from sqlalchemy.orm import Session
from redis.asyncio import Redis
from repositories.repo_sub_items import (get_sub_items_by_category, create_sub_item,get_sub_item_by_id, delete_sub_item, update_sub_item, update_sub_item_quantity)
from repositories.repo_items import get_item_by_id
from model import SubItemOut

async def invalidate_sub_item_cache(redis: Redis, sub_item_id: int, category_id: int, user_id: int):
    await redis.delete(f"sub_item:{sub_item_id}")
    await redis.delete(f"item:{category_id}")

    async for key in redis.scan_iter(f"items:{user_id}:*"):
        await redis.delete(key)

async def get_category_sub_items(db: Session, category_id: int, user_id: int):
    category = get_item_by_id(db, category_id)

    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    if category.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")

    subs = get_sub_items_by_category(db, category_id)

    return [SubItemOut.model_validate(s).model_dump() for s in subs]

async def add_sub_item_service(db: Session, redis: Redis, category_id: int, sub_item, user_id: int):
    category = get_item_by_id(db, category_id)

    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    if category.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")

    new_sub = create_sub_item(db, sub_item.name, category_id)
    await invalidate_sub_item_cache(redis, new_sub.id, category_id, user_id)

    return SubItemOut.model_validate(new_sub).model_dump()

async def delete_sub_item_service(db: Session, redis: Redis, category_id: int, sub_item_id: int, user_id: int):
    category = get_item_by_id(db, category_id)

    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    if category.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")

    sub = get_sub_item_by_id(db, sub_item_id)
    if not sub:
        raise HTTPException(status_code=404, detail="Sub-item not found")

    delete_sub_item(db, sub)
    await invalidate_sub_item_cache(redis, sub_item_id, category_id, user_id)

async def update_sub_item_service(db: Session, redis: Redis, category_id: int, sub_item_id: int, updated, user_id: int):
    category = get_item_by_id(db, category_id)

    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    if category.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")

    sub = get_sub_item_by_id(db, sub_item_id)

    if not sub:
        raise HTTPException(status_code=404, detail="Sub-item not found")

    sub.name = updated.name
    updated_sub = update_sub_item(db, sub)
    await invalidate_sub_item_cache(redis, sub_item_id, category_id, user_id)

    return SubItemOut.model_validate(updated_sub).model_dump()

async def update_quantity_service(db: Session, category_id: int, sub_item_id: int, new_quantity: int, user_id: int):
    category = get_item_by_id(db, category_id)

    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    if category.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")

    sub = get_sub_item_by_id(db, sub_item_id)

    if not sub:
        raise HTTPException(status_code=404, detail="Sub-item not found")

    if new_quantity < 0:
        raise HTTPException(status_code=400, detail="Quantity cannot be negative")
    updated = update_sub_item_quantity(db, sub, new_quantity)

    return SubItemOut.model_validate(updated).model_dump()
