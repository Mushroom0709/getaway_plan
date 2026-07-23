# S7: Hotels CRUD

## Goal

实现 hotels 完整 CRUD。支持按 city 筛选，features 用 JSON 字段。

## Recipe

### File: backend/app/models/hotel.py
```python
from sqlalchemy import Column, Integer, String, Text, Date, DateTime, ForeignKey, Numeric, JSON
from app.models.trip import Base

class Hotel(Base):
    __tablename__ = "hotels"
    id = Column(Integer, primary_key=True, autoincrement=True)
    trip_id = Column(Integer, ForeignKey("trips.id", ondelete="CASCADE"), nullable=False)
    spot_id = Column(Integer, ForeignKey("spots.id", ondelete="SET NULL"), nullable=True)
    city = Column(String(100), nullable=False)
    name = Column(String(300), nullable=False)
    brand = Column(String(200), nullable=True)
    rating = Column(Numeric(2, 1), nullable=True)
    opened_year = Column(Integer, nullable=True)
    price_per_room = Column(Numeric(10, 2), nullable=True)
    room_type = Column(String(200), nullable=True)
    features = Column(JSON, nullable=True)
    check_in_date = Column(Date, nullable=True)
    check_out_date = Column(Date, nullable=True)
    lng = Column(Numeric(10, 6), nullable=True)
    lat = Column(Numeric(10, 6), nullable=True)
    phone = Column(String(50), nullable=True)
    cover_image = Column(String(500), nullable=True)
    notes = Column(Text, nullable=True)
```

### File: backend/app/schemas/hotel.py
Standard Create/Update/Response schemas with features as Optional[list[str]].

### File: backend/app/routers/hotels.py
Standard CRUD: list(GET /api/trips/{trip_id}/hotels with ?city= filter), create, update, delete.

### File: backend/app/main.py
Add `from app.routers.hotels import router as hotel_router` and `app.include_router(hotel_router)`.

## Verification

```bash
cd /Users/mushroom/Documents/ai/hermes/projects/getaway_plan_v1/backend
.venv/bin/python -c "import ast; ast.parse(open('app/models/hotel.py').read())" && echo "✅ hotel model"
.venv/bin/python -c "import ast; ast.parse(open('app/routers/hotels.py').read())" && echo "✅ hotel router"
```