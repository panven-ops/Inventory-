from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Base
from mixins import BaseModelMixin

class UserDB(Base, BaseModelMixin):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String, index=True)
    failed_attempts = Column(Integer, default=0)
    lock_until = Column(DateTime(timezone=True), nullable=True)
    is_admin = Column(Boolean, default=False, nullable=False)
class ItemDB(Base, BaseModelMixin):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    sub_items = relationship("SubItemDB", backref="category", cascade="all, delete")

class SubItemDB(Base, BaseModelMixin):
    __tablename__ = "sub_items"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    quantity = Column(Integer, default=0)  # ← νέο
    category_id = Column(Integer, ForeignKey("items.id"))

class LogDB(Base, BaseModelMixin):
    __tablename__ = "logs"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    action = Column(String, nullable=False)
    ip_address = Column(String, nullable=True)
    endpoint = Column(String, nullable=True)
    status_code = Column(Integer, nullable=True)
    details = Column(String, nullable=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
