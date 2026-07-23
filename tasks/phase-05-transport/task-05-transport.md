# S6: 出行信息 — Flights + Highspeed Rails + Rental Cars

## Goal

实现三个出行资源模块的完整 CRUD：flights、highspeed_rails、rental_cars。

## Acceptance Criteria

- [ ] POST/GET /api/trips/{trip_id}/flights + PUT/DELETE /api/flights/{id}
- [ ] POST/GET /api/trips/{trip_id}/rails + PUT/DELETE /api/rails/{id}
- [ ] POST/GET /api/trips/{trip_id}/cars + PUT/DELETE /api/cars/{id}

## Recipe

### 文件 1: backend/app/models/flight.py
```python
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Numeric
from app.models.trip import Base

class Flight(Base):
    __tablename__ = "flights"
    id = Column(Integer, primary_key=True, autoincrement=True)
    trip_id = Column(Integer, ForeignKey("trips.id", ondelete="CASCADE"), nullable=False)
    flight_no = Column(String(20), nullable=False)
    airline = Column(String(100), nullable=True)
    departure_city = Column(String(100), nullable=False)
    departure_airport = Column(String(200), nullable=True)
    arrival_city = Column(String(100), nullable=False)
    arrival_airport = Column(String(200), nullable=True)
    departure_time = Column(DateTime, nullable=False)
    arrival_time = Column(DateTime, nullable=False)
    duration_min = Column(Integer, nullable=True)
    price = Column(Numeric(10, 2), nullable=True)
    seat_class = Column(String(50), nullable=True)
    booking_link = Column(String(500), nullable=True)
    notes = Column(Text, nullable=True)
```

### 文件 2: backend/app/models/highspeed_rail.py
```python
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Numeric
from app.models.trip import Base

class HighspeedRail(Base):
    __tablename__ = "highspeed_rails"
    id = Column(Integer, primary_key=True, autoincrement=True)
    trip_id = Column(Integer, ForeignKey("trips.id", ondelete="CASCADE"), nullable=False)
    train_no = Column(String(20), nullable=False)
    departure_city = Column(String(100), nullable=False)
    departure_station = Column(String(200), nullable=False)
    arrival_city = Column(String(100), nullable=False)
    arrival_station = Column(String(200), nullable=False)
    departure_time = Column(DateTime, nullable=False)
    arrival_time = Column(DateTime, nullable=False)
    duration_min = Column(Integer, nullable=True)
    price = Column(Numeric(10, 2), nullable=True)
    seat_class = Column(String(50), nullable=True)
    booking_link = Column(String(500), nullable=True)
    notes = Column(Text, nullable=True)
```

### 文件 3: backend/app/models/rental_car.py
```python
from sqlalchemy import Column, Integer, String, Text, ForeignKey, Numeric
from app.models.trip import Base

class RentalCar(Base):
    __tablename__ = "rental_cars"
    id = Column(Integer, primary_key=True, autoincrement=True)
    trip_id = Column(Integer, ForeignKey("trips.id", ondelete="CASCADE"), nullable=False)
    platform = Column(String(100), nullable=True)
    car_name = Column(String(200), nullable=False)
    daily_price = Column(Numeric(10, 2), nullable=True)
    engine = Column(String(100), nullable=True)
    seats = Column(Integer, nullable=True)
    trunk = Column(String(100), nullable=True)
    notes = Column(Text, nullable=True)
```

### 文件 4-6: schemas + routers
Create standard CRUD schemas and routers for all three models, same pattern as S3/S4. Each router has prefix="/api" with list/create under /trips/{trip_id}/[resource] and update/delete under /[resource]/{id}.

### 文件 7: backend/app/main.py — 更新
Add imports and include_router for flight_router, rail_router, car_router.

## Verification
```bash
cd /Users/mushroom/Documents/ai/hermes/projects/getaway_plan_v1/backend
for f in app/models/flight.py app/models/highspeed_rail.py app/models/rental_car.py; do
  .venv/bin/python -c "import ast; ast.parse(open('$f').read())" && echo "✅ $f" || echo "❌ $f"
done
```