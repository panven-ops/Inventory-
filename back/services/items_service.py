import json
from fastapi import HTTPException

from repositories.repo_items import (
    get_items_by_user,
    get_item_by_id,
    create_item,
    delete_item,
    update_item,
    get_total_items
)

from model import ItemOut
from redis_client import redis_client


# CACHE KEYS

def items_list_key(user_id, skip, limit):
    return f"items:{user_id}:{skip}:{limit}"


def item_key(item_id):
    return f"item:{item_id}"


# CACHE INVALIDATION

def invalidate_user_cache(user_id):
    for key in redis_client.scan_iter(f"items:{user_id}:*"):
        redis_client.delete(key)


# GET USER ITEMS (cached)

def get_user_items(db, user_id, skip, limit):
    cache_key = items_list_key(user_id, skip, limit)

    cached = redis_client.get(cache_key)
    if cached:
        return json.loads(cached)

    items = get_items_by_user(db, user_id, skip, limit)
    total = get_total_items(db, user_id)

    result = {
        "data": [
            ItemOut.model_validate(i).model_dump()
            for i in items
        ],
        "total": total,
        "skip": skip,
        "limit": limit,
        "pages": -(-total // limit)
    }

    redis_client.setex(cache_key, 60, json.dumps(result))

    return result


# GET SINGLE ITEM (cached)

def get_single_item(db, item_id):
    cache_key = item_key(item_id)

    cached = redis_client.get(cache_key)
    if cached:
        return json.loads(cached)

    item = get_item_by_id(db, item_id)

    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    data = ItemOut.model_validate(item).model_dump()

    redis_client.setex(cache_key, 60, json.dumps(data))

    return data


# CREATE ITEM

def add_item_service(db, item, user_id):
    new_item = create_item(db, item.name, user_id)

    invalidate_user_cache(user_id)

    return ItemOut.model_validate(new_item).model_dump()


# DELETE ITEM

def delete_item_service(db, item_id, user_id):
    item = get_item_by_id(db, item_id)

    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    if item.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")

    delete_item(db, item)

    redis_client.delete(item_key(item_id))
    invalidate_user_cache(user_id)


# UPDATE ITEM

def update_item_service(db, item_id, updated_item, user_id):
    item = get_item_by_id(db, item_id)

    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    if item.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")

    item.name = updated_item.name
    updated = update_item(db, item)

    redis_client.delete(item_key(item_id))
    invalidate_user_cache(user_id)

    return ItemOut.model_validate(updated).model_dump()
