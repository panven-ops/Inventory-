from fastapi import APIRouter, Depends, Request, Query
from sqlalchemy.orm import Session
from redis.asyncio import Redis
from database import get_db
from redis_client import get_redis
from auth import get_current_user
from model import Item, PaginatedItems
from rate_limit import (items_read_limiter, items_write_limiter, items_delete_limiter)
from services.items_service import (get_user_items, get_single_item,add_item_service, delete_item_service, update_item_service)

router = APIRouter()

@router.get("/items", response_model=PaginatedItems)
async def get_items(request: Request, _: None = Depends(items_read_limiter), user_id: int = Depends(get_current_user),db: Session = Depends(get_db), redis: Redis = Depends(get_redis), skip: int = Query(0, ge=0), limit: int = Query(10, ge=1, le=100)):

    return await get_user_items(db, redis, user_id, skip, limit)

@router.get("/items/{item_id}")
async def get_item(item_id: int,request: Request, _: None = Depends(items_read_limiter), user_id: int = Depends(get_current_user), db: Session = Depends(get_db), redis: Redis = Depends(get_redis)):

    return await get_single_item(db, redis, item_id)

@router.post("/items")
async def add_item(item: Item,request: Request, _: None = Depends(items_write_limiter), user_id: int = Depends(get_current_user), db: Session = Depends(get_db), redis: Redis = Depends(get_redis),):

    return await add_item_service(db, redis, item, user_id)

@router.delete("/items/{item_id}")
async def delete_item(item_id: int, request: Request, _: None = Depends(items_delete_limiter), user_id: int = Depends(get_current_user), db: Session = Depends(get_db), redis: Redis = Depends(get_redis)):

    await delete_item_service(db, redis, item_id, user_id)

    return {"message": "Deleted"}

@router.put("/items/{item_id}")
async def update_item(item_id: int, item: Item, request: Request, _: None = Depends(items_write_limiter), user_id: int = Depends(get_current_user), db: Session = Depends(get_db), redis: Redis = Depends(get_redis)):

    return await update_item_service(db, redis, item_id, item, user_id)
