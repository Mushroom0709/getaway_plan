# S3: 旅行核心 — Trips + Days CRUD

## Goal

实现 trips 和 days 的完整 CRUD API。trips 支持嵌套查询，days 支持按 trip_id 筛选。

## Acceptance Criteria

- [ ] POST /api/trips 创建旅行，返回 201
- [ ] GET /api/trips 返回所有旅行列表
- [ ] GET /api/trips/{id} 返回嵌套数据（含 days）
- [ ] PUT /api/trips/{id} 更新旅行
- [ ] DELETE /api/trips/{id} 级联删除所有关联数据
- [ ] POST /api/trips/{trip_id}/days 创建每日行程
- [ ] GET /api/trips/{trip_id}/days 返回该旅行所有天
- [ ] PUT/DELETE /api/days/{id} 更新/删除

## Recipe

### 文件 1: backend/app/models/trip.py
```python
from sqlalchemy import Column, Integer, String, Text, Date, DateTime, Enum
from sqlalchemy.orm import DeclarativeBase, relationship
from datetime import datetime, timezone
import enum

class Base(DeclarativeBase):
    pass

class TripStatus(str, enum.Enum):
    planning = "planning"
    active = "active"
    completed = "completed"

class Trip(Base):
    __tablename__ = "trips"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)
    status = Column(Enum(TripStatus), default=TripStatus.planning, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    days = relationship("Day", back_populates="trip", lazy="selectin", cascade="all, delete-orphan")
```

### 文件 2: backend/app/models/day.py
```python
from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.models.trip import Base

class Day(Base):
    __tablename__ = "days"

    id = Column(Integer, primary_key=True, autoincrement=True)
    trip_id = Column(Integer, ForeignKey("trips.id", ondelete="CASCADE"), nullable=False)
    day_number = Column(Integer, nullable=False)
    date = Column(Date, nullable=True)
    title = Column(String(200), nullable=True)
    drive_hours = Column(Numeric(3, 1), nullable=True)
    hotel_city = Column(String(100), nullable=True)
    sort_order = Column(Integer, nullable=False, default=0)

    trip = relationship("Trip", back_populates="days")
```

### 文件 3: backend/app/schemas/trip.py
```python
from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional

class TripCreate(BaseModel):
    name: str
    description: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None

class TripUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    status: Optional[str] = None

class DayResponse(BaseModel):
    id: int
    day_number: int
    date: Optional[date] = None
    title: Optional[str] = None
    drive_hours: Optional[float] = None
    hotel_city: Optional[str] = None
    sort_order: int

    class Config:
        from_attributes = True

class TripResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    status: str
    created_at: datetime
    updated_at: datetime
    days: list[DayResponse] = []

    class Config:
        from_attributes = True

class TripListResponse(BaseModel):
    id: int
    name: str
    status: str
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    created_at: datetime

    class Config:
        from_attributes = True
```

### 文件 4: backend/app/schemas/day.py
```python
from pydantic import BaseModel
from datetime import date
from typing import Optional

class DayCreate(BaseModel):
    day_number: int
    date: Optional[date] = None
    title: Optional[str] = None
    drive_hours: Optional[float] = None
    hotel_city: Optional[str] = None
    sort_order: int = 0

class DayUpdate(BaseModel):
    day_number: Optional[int] = None
    date: Optional[date] = None
    title: Optional[str] = None
    drive_hours: Optional[float] = None
    hotel_city: Optional[str] = None
    sort_order: Optional[int] = None

class DayResponse(BaseModel):
    id: int
    trip_id: int
    day_number: int
    date: Optional[date] = None
    title: Optional[str] = None
    drive_hours: Optional[float] = None
    hotel_city: Optional[str] = None
    sort_order: int

    class Config:
        from_attributes = True
```

### 文件 5: backend/app/routers/trips.py
```python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.deps import get_current_device_id
from app.models.trip import Trip
from app.schemas.trip import TripCreate, TripUpdate, TripResponse, TripListResponse

router = APIRouter(prefix="/api/trips", tags=["trips"], dependencies=[Depends(get_current_device_id)])

@router.get("", response_model=list[TripListResponse])
async def list_trips(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Trip).order_by(Trip.created_at.desc()))
    trips = result.scalars().all()
    return [TripListResponse.model_validate(t) for t in trips]

@router.post("", response_model=TripResponse, status_code=201)
async def create_trip(data: TripCreate, db: AsyncSession = Depends(get_db)):
    trip = Trip(**data.model_dump())
    db.add(trip)
    await db.commit()
    await db.refresh(trip)
    return TripResponse.model_validate(trip)

@router.get("/{trip_id}", response_model=TripResponse)
async def get_trip(trip_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Trip).where(Trip.id == trip_id))
    trip = result.scalar_one_or_none()
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    return TripResponse.model_validate(trip)

@router.put("/{trip_id}", response_model=TripResponse)
async def update_trip(trip_id: int, data: TripUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Trip).where(Trip.id == trip_id))
    trip = result.scalar_one_or_none()
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    for key, val in data.model_dump(exclude_unset=True).items():
        setattr(trip, key, val)
    await db.commit()
    await db.refresh(trip)
    return TripResponse.model_validate(trip)

@router.delete("/{trip_id}", status_code=204)
async def delete_trip(trip_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Trip).where(Trip.id == trip_id))
    trip = result.scalar_one_or_none()
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    await db.delete(trip)
    await db.commit()
```

### 文件 6: backend/app/routers/days.py
```python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.deps import get_current_device_id
from app.models.day import Day
from app.schemas.day import DayCreate, DayUpdate, DayResponse

router = APIRouter(prefix="/api", tags=["days"], dependencies=[Depends(get_current_device_id)])

@router.get("/trips/{trip_id}/days", response_model=list[DayResponse])
async def list_days(trip_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Day).where(Day.trip_id == trip_id).order_by(Day.sort_order))
    days = result.scalars().all()
    return [DayResponse.model_validate(d) for d in days]

@router.post("/trips/{trip_id}/days", response_model=DayResponse, status_code=201)
async def create_day(trip_id: int, data: DayCreate, db: AsyncSession = Depends(get_db)):
    day = Day(trip_id=trip_id, **data.model_dump())
    db.add(day)
    await db.commit()
    await db.refresh(day)
    return DayResponse.model_validate(day)

@router.put("/days/{day_id}", response_model=DayResponse)
async def update_day(day_id: int, data: DayUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Day).where(Day.id == day_id))
    day = result.scalar_one_or_none()
    if not day:
        raise HTTPException(status_code=404, detail="Day not found")
    for key, val in data.model_dump(exclude_unset=True).items():
        setattr(day, key, val)
    await db.commit()
    await db.refresh(day)
    return DayResponse.model_validate(day)

@router.delete("/days/{day_id}", status_code=204)
async def delete_day(day_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Day).where(Day.id == day_id))
    day = result.scalar_one_or_none()
    if not day:
        raise HTTPException(status_code=404, detail="Day not found")
    await db.delete(day)
    await db.commit()
```

### 文件 7: backend/app/main.py — 更新
当前 main.py 只注册了 auth_router。需要添加 trip_router 和 day_router：
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers.auth import router as auth_router
from app.routers.trips import router as trip_router
from app.routers.days import router as day_router

app = FastAPI(title="Getaway Plan API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(trip_router)
app.include_router(day_router)

@app.get("/api/health")
async def health():
    return {"status": "ok"}
```

## Verification

```bash
cd /Users/mushroom/Documents/ai/hermes/projects/getaway_plan_v1
# 语法检查
for f in app/models/trip.py app/models/day.py app/schemas/trip.py app/schemas/day.py app/routers/trips.py app/routers/days.py; do
  .venv/bin/python -c "import ast; ast.parse(open('backend/$f').read())" && echo "✅ $f" || echo "❌ $f"
done
```