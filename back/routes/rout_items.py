from fastapi import APIRouter, Depends, Request, Query
from sqlalchemy.orm import Session
from database import get_db
from auth import get_current_user
from model import Item, PaginatedItems
from lim import limiter
from services.items_service import (get_user_items,get_single_item,add_item_service,delete_item_service,update_item_service)

router = APIRouter()


@router.get("/items", response_model=PaginatedItems)
@limiter.limit("10/minute")
def get_items(
    request: Request,
    user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100)
):
    return get_user_items(db, user_id, skip, limit)


@router.get("/items/{item_id}")
def get_item(item_id: int, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    return get_single_item(db, item_id)


@router.post("/items")
def add_item(item: Item, user_id: int = Depends(get_current_user), db: Session = Depends(get_db)):
    return add_item_service(db, item, user_id)


@router.delete("/items/{item_id}")
def delete_item(item_id: int, user_id: int = Depends(get_current_user), db: Session = Depends(get_db)):
    delete_item_service(db, item_id, user_id)
    return {"message": "Deleted"}


@router.put("/items/{item_id}")
def update_item(item_id: int, item: Item, user_id: int = Depends(get_current_user), db: Session = Depends(get_db)):
    return update_item_service(db, item_id, item, user_id) 
