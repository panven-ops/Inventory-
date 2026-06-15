from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from auth import get_current_user
from model import SubItem, SubItemQuantityUpdate
from services.service_sub_items import (
    get_category_sub_items, add_sub_item_service,
    delete_sub_item_service, update_sub_item_service, update_quantity_service
)

router = APIRouter()

@router.get("/items/{category_id}/sub-items")
def get_sub_items(category_id: int, user_id: int = Depends(get_current_user), db: Session = Depends(get_db)):
    return get_category_sub_items(db, category_id, user_id)

@router.post("/items/{category_id}/sub-items")
def add_sub_item(category_id: int, sub_item: SubItem, user_id: int = Depends(get_current_user), db: Session = Depends(get_db)):
    return add_sub_item_service(db, category_id, sub_item, user_id)

@router.delete("/items/{category_id}/sub-items/{sub_item_id}")
def delete_sub_item(category_id: int, sub_item_id: int, user_id: int = Depends(get_current_user), db: Session = Depends(get_db)):
    delete_sub_item_service(db, category_id, sub_item_id, user_id)
    return {"message": "Deleted"}

@router.put("/items/{category_id}/sub-items/{sub_item_id}")
def update_sub_item(category_id: int, sub_item_id: int, sub_item: SubItem, user_id: int = Depends(get_current_user), db: Session = Depends(get_db)):
    return update_sub_item_service(db, category_id, sub_item_id, sub_item, user_id)

@router.patch("/items/{category_id}/sub-items/{sub_item_id}/quantity")
def update_quantity(
    category_id: int,
    sub_item_id: int,
    payload: SubItemQuantityUpdate,
    user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return update_quantity_service(db, category_id, sub_item_id, payload.quantity, user_id)
