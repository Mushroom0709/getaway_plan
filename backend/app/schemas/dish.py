from pydantic import BaseModel
from typing import Optional
from datetime import time

class DishCreate(BaseModel):
    name: str
    price: Optional[float] = None
    description: Optional[str] = None
    image: Optional[str] = None
    is_signature: bool = False

class DishUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    description: Optional[str] = None
    image: Optional[str] = None
    is_signature: Optional[bool] = None

class DishResponse(BaseModel):
    id: int
    restaurant_id: int
    name: str
    price: Optional[float] = None
    description: Optional[str] = None
    image: Optional[str] = None
    is_signature: bool = False

    class Config:
        from_attributes = True