from pydantic import BaseModel
from typing import Optional

class DailyMealCreate(BaseModel):
    restaurant_id: int
    meal_type: str
    notes: Optional[str] = None

class DailyMealResponse(BaseModel):
    id: int
    day_id: int
    restaurant_id: int
    meal_type: str
    notes: Optional[str] = None

    class Config:
        from_attributes = True
