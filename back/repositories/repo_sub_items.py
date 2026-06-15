from sqlalchemy.orm import Session
from db_models import SubItemDB

def get_sub_items_by_category(db: Session, category_id: int):

    return db.query(SubItemDB).filter(SubItemDB.category_id == category_id).all()

def create_sub_item(db: Session, name: str, category_id: int):
    sub = SubItemDB(name=name, category_id=category_id)
    db.add(sub)
    db.commit()
    db.refresh(sub)

    return sub

def get_sub_item_by_id(db: Session, sub_item_id: int):

    return db.query(SubItemDB).filter(SubItemDB.id == sub_item_id).first()

def delete_sub_item(db: Session, sub_item):
    db.delete(sub_item)
    db.commit()

def update_sub_item(db: Session, sub_item):
    db.commit()
    db.refresh(sub_item)

    return sub_item

def update_sub_item_quantity(db: Session, sub_item, new_quantity: int):
    sub_item.quantity = new_quantity
    db.commit()
    db.refresh(sub_item)

    return sub_item
