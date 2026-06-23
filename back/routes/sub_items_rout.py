from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from redis.asyncio import Redis
from database import get_db
from redis_client import get_redis
from auth import get_current_user
from model import SubItem, SubItemQuantityUpdate
from rate_limit import (sub_items_read_limiter, items_write_limiter, items_delete_limiter)
from services.service_sub_items import (get_category_sub_items, add_sub_item_service,delete_sub_item_service, update_sub_item_service, update_quantity_service)

router = APIRouter()

@router.get("/items/{category_id}/sub-items")
async def get_sub_items(category_id: int,request: Request,_: None = Depends(sub_items_read_limiter),user_id: int = Depends(get_current_user),db: Session = Depends(get_db)):

    return await get_category_sub_items(db, category_id, user_id)

@router.post("/items/{category_id}/sub-items")
async def add_sub_item(category_id: int,sub_item: SubItem,request: Request,_: None = Depends(items_write_limiter),user_id: int = Depends(get_current_user),db: Session = Depends(get_db),redis: Redis = Depends(get_redis)):

    return await add_sub_item_service(db, redis, category_id, sub_item, user_id)

@router.delete("/items/{category_id}/sub-items/{sub_item_id}")
async def delete_sub_item(category_id: int,sub_item_id: int,request: Request,_: None = Depends(items_delete_limiter),user_id: int = Depends(get_current_user),db: Session = Depends(get_db),redis: Redis = Depends(get_redis)):

    await delete_sub_item_service(db, redis, category_id, sub_item_id, user_id)

    return {"message": "Deleted"}

@router.put("/items/{category_id}/sub-items/{sub_item_id}")
async def update_sub_item(category_id: int,sub_item_id: int,sub_item: SubItem,request: Request,_: None = Depends(items_write_limiter),user_id: int = Depends(get_current_user),db: Session = Depends(get_db),redis: Redis = Depends(get_redis)):

    return await update_sub_item_service(db, redis, category_id, sub_item_id, sub_item, user_id)

@router.patch("/items/{category_id}/sub-items/{sub_item_id}/quantity")
async def update_quantity(category_id: int,sub_item_id: int,payload: SubItemQuantityUpdate,request: Request,_: None = Depends(items_write_limiter),user_id: int = Depends(get_current_user),db: Session = Depends(get_db)):

    return await update_quantity_service(db, category_id, sub_item_id, payload.quantity, user_id)
