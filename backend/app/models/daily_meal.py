from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, Numeric, JSON, Date, Enum as SAEnum
from app.models.trip import Base
import enum
from datetime import datetime, timezone

class MealType(str, enum.Enum):
    breakfast = "breakfast"
    lunch = "lunch"
    dinner = "dinner"
    snack = "snack"

class DailyMeal(Base):
    __tablename__ = "daily_meals"
    id = Column(Integer, primary_key=True, autoincrement=True)
    day_id = Column(Integer, ForeignKey("days.id", ondelete="CASCADE"), nullable=False)
    restaurant_id = Column(Integer, ForeignKey("restaurants.id", ondelete="CASCADE"), nullable=False)
    meal_type = Column(SAEnum(MealType), nullable=False)
    notes = Column(Text, nullable=True)