from sqlalchemy import Column, Integer, String, Text, ForeignKey, Boolean, Numeric
from app.models.trip import Base

class Dish(Base):
    __tablename__ = "dishes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    restaurant_id = Column(Integer, ForeignKey("restaurants.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(200), nullable=False)
    price = Column(Numeric(10, 2), nullable=True)
    description = Column(Text, nullable=True)
    image = Column(String(500), nullable=True)
    is_signature = Column(Boolean, default=False)
