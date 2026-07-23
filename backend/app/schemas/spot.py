from pydantic import BaseModel, Field
from datetime import time, datetime
from typing import Optional, Literal

SpotCategoryLiteral = Literal["airport", "highspeed_rail", "train", "scenic", "photo", "hotel", "restaurant", "other"]

class SpotCreate(BaseModel):
    day_id: Optional[int] = None
    name: str
    lng: float
    lat: float
    category: SpotCategoryLiteral = "other"
    is_nav_point: bool = False
    nav_order: Optional[int] = None
    arrival_time: Optional[time] = None
    description: Optional[str] = None
    intro: Optional[str] = None

class SpotUpdate(BaseModel):
    day_id: Optional[int] = None
    name: Optional[str] = None
    lng: Optional[float] = None
    lat: Optional[float] = None
    category: Optional[SpotCategoryLiteral] = None
    is_nav_point: Optional[bool] = None
    nav_order: Optional[int] = None
    arrival_time: Optional[time] = None
    description: Optional[str] = None
    intro: Optional[str] = None

class SpotResponse(BaseModel):
    id: int
    trip_id: int
    day_id: Optional[int] = None
    name: str
    lng: float
    lat: float
    category: str
    is_nav_point: bool
    nav_order: Optional[int] = None
    arrival_time: Optional[time] = None
    description: Optional[str] = None
    intro: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class SpotReorderItem(BaseModel):
    id: int
    nav_order: int
