from sqlalchemy.orm import Session
from db_models import ItemDB

def get_items_by_user(db: Session, user_id: int, skip: int, limit: int):
    return (
        db.query(ItemDB)
        .filter(ItemDB.user_id == user_id)
        .order_by(ItemDB.id)
        .offset(skip)
        .limit(limit)
        .all()
    )

def get_item_by_id(db: Session, item_id: int):
    return db.query(ItemDB).filter(ItemDB.id == item_id).first()

def create_item(db: Session, name: str, user_id: int):
    item = ItemDB(name=name, user_id=user_id)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

def delete_item(db: Session, item):
    db.delete(item)
    db.commit()

def update_item(db: Session, item):
    db.commit()
    db.refresh(item)
    return item

def get_total_items(db: Session, user_id: int):
    return db.query(ItemDB).filter(ItemDB.user_id == user_id).count()