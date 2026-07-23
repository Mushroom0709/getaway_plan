from pydantic import BaseModel
from typing import Optional

class BudgetItemCreate(BaseModel):
    category: str
    item: str
    unit_price: Optional[float] = None
    quantity: int = 1
    subtotal: Optional[float] = None
    note: Optional[str] = None

class BudgetItemUpdate(BaseModel):
    category: Optional[str] = None
    item: Optional[str] = None
    unit_price: Optional[float] = None
    quantity: Optional[int] = None
    subtotal: Optional[float] = None
    note: Optional[str] = None

class BudgetItemResponse(BaseModel):
    id: int
    trip_id: int
    category: str
    item: str
    unit_price: Optional[float] = None
    quantity: int = 1
    subtotal: Optional[float] = None
    note: Optional[str] = None

    class Config:
        from_attributes = True
