# S4: 坐标点 — Spots CRUD + 导航点排序

## Goal

实现 spots 完整 CRUD API + 批量导航点排序。支持按 day_id、category、is_nav_point 筛选。

## Acceptance Criteria

- [ ] POST /api/trips/{trip_id}/spots 创建坐标点（含 category 枚举验证）
- [ ] GET /api/trips/{trip_id}/spots 支持筛选 day_id、category、is_nav_point
- [ ] PUT /api/spots/{id} 更新坐标点
- [ ] DELETE /api/spots/{id} 删除
- [ ] PUT /api/trips/{trip_id}/spots/reorder 批量更新 nav_order

## Recipe

### 文件 1: backend/app/models/spot.py
```python
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, Numeric, Time, Enum
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.models.trip import Base
import enum

class SpotCategory(str, enum.Enum):
    airport = "airport"
    highspeed_rail = "highspeed_rail"
    train = "train"
    scenic = "scenic"
    photo = "photo"
    hotel = "hotel"
    restaurant = "restaurant"
    other = "other"

class Spot(Base):
    __tablename__ = "spots"

    id = Column(Integer, primary_key=True, autoincrement=True)
    trip_id = Column(Integer, ForeignKey("trips.id", ondelete="CASCADE"), nullable=False)
    day_id = Column(Integer, ForeignKey("days.id", ondelete="SET NULL"), nullable=True)
    name = Column(String(200), nullable=False)
    lng = Column(Numeric(10, 6), nullable=False)
    lat = Column(Numeric(10, 6), nullable=False)
    category = Column(Enum(SpotCategory), nullable=False, default=SpotCategory.other)
    is_nav_point = Column(Boolean, default=False)
    nav_order = Column(Integer, nullable=True)
    arrival_time = Column(Time, nullable=True)
    description = Column(String(500), nullable=True)
    intro = Column(Text, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
```

### 文件 2: backend/app/schemas/spot.py
```python
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
```

### 文件 3: backend/app/routers/spots.py
```python
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional
from app.database import get_db
from app.deps import get_current_device_id
from app.models.spot import Spot
from app.schemas.spot import SpotCreate, SpotUpdate, SpotResponse, SpotReorderItem

router = APIRouter(prefix="/api", tags=["spots"], dependencies=[Depends(get_current_device_id)])

@router.get("/trips/{trip_id}/spots", response_model=list[SpotResponse])
async def list_spots(
    trip_id: int,
    day_id: Optional[int] = Query(None),
    category: Optional[str] = Query(None),
    is_nav_point: Optional[bool] = Query(None),
    db: AsyncSession = Depends(get_db),
):
    stmt = select(Spot).where(Spot.trip_id == trip_id)
    if day_id is not None:
        stmt = stmt.where(Spot.day_id == day_id)
    if category is not None:
        stmt = stmt.where(Spot.category == category)
    if is_nav_point is not None:
        stmt = stmt.where(Spot.is_nav_point == is_nav_point)
    stmt = stmt.order_by(Spot.nav_order.is_(None), Spot.nav_order, Spot.created_at)
    result = await db.execute(stmt)
    spots = result.scalars().all()
    return [SpotResponse.model_validate(s) for s in spots]

@router.post("/trips/{trip_id}/spots", response_model=SpotResponse, status_code=201)
async def create_spot(trip_id: int, data: SpotCreate, db: AsyncSession = Depends(get_db)):
    spot = Spot(trip_id=trip_id, **data.model_dump())
    db.add(spot)
    await db.commit()
    await db.refresh(spot)
    return SpotResponse.model_validate(spot)

@router.put("/spots/{spot_id}", response_model=SpotResponse)
async def update_spot(spot_id: int, data: SpotUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Spot).where(Spot.id == spot_id))
    spot = result.scalar_one_or_none()
    if not spot:
        raise HTTPException(status_code=404, detail="Spot not found")
    for key, val in data.model_dump(exclude_unset=True).items():
        setattr(spot, key, val)
    await db.commit()
    await db.refresh(spot)
    return SpotResponse.model_validate(spot)

@router.delete("/spots/{spot_id}", status_code=204)
async def delete_spot(spot_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Spot).where(Spot.id == spot_id))
    spot = result.scalar_one_or_none()
    if not spot:
        raise HTTPException(status_code=404, detail="Spot not found")
    await db.delete(spot)
    await db.commit()

@router.put("/trips/{trip_id}/spots/reorder", response_model=list[SpotResponse])
async def reorder_spots(trip_id: int, items: list[SpotReorderItem], db: AsyncSession = Depends(get_db)):
    if not items:
        raise HTTPException(status_code=400, detail="Empty reorder list")
    ids = [item.id for item in items]
    result = await db.execute(select(Spot).where(Spot.id.in_(ids), Spot.trip_id == trip_id))
    spots = {s.id: s for s in result.scalars().all()}
    for item in items:
        if item.id in spots:
            spots[item.id].nav_order = item.nav_order
    await db.commit()
    return [SpotResponse.model_validate(s) for s in spots.values()]
```

### 文件 4: backend/app/main.py — 更新
Add `from app.routers.spots import router as spot_router` and `app.include_router(spot_router)`.

## Verification

```bash
cd /Users/mushroom/Documents/ai/hermes/projects/getaway_plan_v1/backend
for f in app/models/spot.py app/schemas/spot.py app/routers/spots.py; do
  .venv/bin/python -c "import ast; ast.parse(open('$f').read())" && echo "✅ $f" || echo "❌ $f"
done
```