from sqlalchemy import Column, Integer, String, Text, ForeignKey, Numeric, Enum as SAEnum
from app.models.trip import Base
import enum

class BudgetCategory(str, enum.Enum):
    flight = "flight"
    hotel = "hotel"
    car = "car"
    food = "food"
    ticket = "ticket"
    rail = "rail"
    other = "other"

class BudgetItem(Base):
    __tablename__ = "budget_items"
    id = Column(Integer, primary_key=True, autoincrement=True)
    trip_id = Column(Integer, ForeignKey("trips.id", ondelete="CASCADE"), nullable=False)
    category = Column(SAEnum(BudgetCategory), nullable=False)
    item = Column(String(300), nullable=False)
    unit_price = Column(Numeric(10, 2), nullable=True)
    quantity = Column(Integer, default=1)
    subtotal = Column(Numeric(10, 2), nullable=True)
    note = Column(Text, nullable=True)