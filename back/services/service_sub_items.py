from fastapi import HTTPException
from repositories.repo_sub_items import (
    get_sub_items_by_category, create_sub_item,
    get_sub_item_by_id, delete_sub_item, update_sub_item, update_sub_item_quantity
)
from repositories.repo_items import get_item_by_id
from model import SubItemOut

def get_category_sub_items(db, category_id, user_id):
    # Πρώτα ελέγχουμε ότι η κατηγορία ανήκει στον χρήστη
    category = get_item_by_id(db, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    if category.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")
    subs = get_sub_items_by_category(db, category_id)
    return [SubItemOut.model_validate(s).model_dump() for s in subs]

def add_sub_item_service(db, category_id, sub_item, user_id):
    category = get_item_by_id(db, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    if category.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")
    new_sub = create_sub_item(db, sub_item.name, category_id)
    return SubItemOut.model_validate(new_sub).model_dump()

def delete_sub_item_service(db, category_id, sub_item_id, user_id):
    category = get_item_by_id(db, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    if category.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")
    sub = get_sub_item_by_id(db, sub_item_id)
    if not sub:
        raise HTTPException(status_code=404, detail="Sub-item not found")
    delete_sub_item(db, sub)

def update_sub_item_service(db, category_id, sub_item_id, updated, user_id):
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
    return SubItemOut.model_validate(updated_sub).model_dump()

def update_quantity_service(db, category_id, sub_item_id, new_quantity, user_id):
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
