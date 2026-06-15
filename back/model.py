from pydantic import BaseModel, field_validator
from typing import List
from sanitize import sanitize_string, sanitize_username, sanitize_password

class Item(BaseModel):
    name: str

    @field_validator("name")
    @classmethod
    def validate_name(cls, v):
        return sanitize_string(v)

class SubItem(BaseModel):
    name: str
    quantity: int = 0

    @field_validator("name")
    @classmethod
    def validate_name(cls, v):
        return sanitize_string(v)

    @field_validator("quantity")
    @classmethod
    def validate_quantity(cls, v):
        if v < 0:
            raise ValueError("Quantity can't be negative")
        if v > 999999:
            raise ValueError("Invalid quantity")
        return v

class SubItemOut(BaseModel):
    id: int
    name: str
    quantity: int
    category_id: int

    class Config:
        from_attributes = True

class SubItemQuantityUpdate(BaseModel):
    quantity: int

class ItemOut(BaseModel):
    id: int
    name: str
    sub_items: List[SubItemOut] = []


    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    username: str
    password: str

    @field_validator("username")
    @classmethod
    def validate_username(cls, v):
        return sanitize_username(v)

    @field_validator("password")
    @classmethod
    def validate_password(cls, v):
        return sanitize_password(v)

class UserLogin(BaseModel):
    username: str
    password: str

    @field_validator("username")
    @classmethod
    def validate_username(cls, v):
        return sanitize_username(v)

    @field_validator("password")
    @classmethod
    def validate_password(cls, v):
        return sanitize_password(v)

class PaginatedItems(BaseModel):
    data: List[ItemOut]
    total: int
    skip: int
    limit: int
    pages: int
