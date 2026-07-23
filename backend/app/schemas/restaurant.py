from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date, datetime
from decimal import Decimal

class RestaurantCreate(BaseModel):
    spot_id: Optional[int] = None
    city: str
    name: str
    address: Optional[str] = None
    lng: Optional[float] = None
    lat: Optional[float] = None
    rating: Optional[float] = None
    avg_price: Optional[float] = None
    cuisine: Optional[str] = None
    phone: Optional[str] = None
    opening_hours: Optional[str] = None
    maps_url: Optional[str] = None
    cover_image: Optional[str] = None
    notes: Optional[str] = None

class RestaurantUpdate(BaseModel):
    spot_id: Optional[int] = None
    city: Optional[str] = None
    name: Optional[str] = None
    address: Optional[str] = None
    lng: Optional[float] = None
    lat: Optional[float] = None
    rating: Optional[float] = None
    avg_price: Optional[float] = None
    cuisine: Optional[str] = None
    phone: Optional[str] = None
    opening_hours: Optional[str] = None
    maps_url: Optional[str] = None
    cover_image: Optional[str] = None
    notes: Optional[str] = None

class DishResponse(BaseModel):
    id: int
    name: str
    price: Optional[float] = None
    description: Optional[str] = None
    image: Optional[str] = None
    is_signature: bool = False

    class Config:
        from_attributes = True

class RestaurantResponse(BaseModel):
    id: int
    trip_id: int
    spot_id: Optional[int] = None
    city: str
    name: str
    address: Optional[str] = None
    lng: Optional[float] = None
    lat: Optional[float] = None
    rating: Optional[float] = None
    avg_price: Optional[float] = None
    cuisine: Optional[str] = None
    phone: Optional[str] = None
    opening_hours: Optional[str] = None
    maps_url: Optional[str] = None
    cover_image: Optional[str] = None
    notes: Optional[str] = None
    dishes: List[DishResponse] = []

    class Config:
        from_attributes = True