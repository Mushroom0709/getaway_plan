# S5: 路线规划 — 高德 REST API + route_segments

## Goal

实现路线规划服务：route_service 调用高德 REST API 获取 driving 路线，存入 route_segments 表。

## Acceptance Criteria

- [ ] POST /api/trips/{trip_id}/routes/plan 调用高德 REST API，返回 polyline
- [ ] GET /api/trips/{trip_id}/routes 返回所有路段
- [ ] DELETE /api/routes/{id}

## Recipe

### 文件 1: backend/app/models/route_segment.py
```python
from sqlalchemy import Column, Integer, String, Text, ForeignKey, Numeric
from app.models.trip import Base

class RouteSegment(Base):
    __tablename__ = "route_segments"

    id = Column(Integer, primary_key=True, autoincrement=True)
    trip_id = Column(Integer, ForeignKey("trips.id", ondelete="CASCADE"), nullable=False)
    from_spot_id = Column(Integer, ForeignKey("spots.id", ondelete="SET NULL"), nullable=True)
    to_spot_id = Column(Integer, ForeignKey("spots.id", ondelete="SET NULL"), nullable=True)
    distance_km = Column(Numeric(8, 2), nullable=True)
    duration_min = Column(Integer, nullable=True)
    polyline = Column(Text, nullable=True)
    color = Column(String(20), nullable=True)
    day_number = Column(Integer, nullable=True)
```

### 文件 2: backend/app/schemas/route_segment.py
```python
from pydantic import BaseModel
from typing import Optional

class RoutePlanRequest(BaseModel):
    from_spot_id: int
    to_spot_id: int
    color: str = "#4caf50"
    day_number: Optional[int] = None

class RouteSegmentResponse(BaseModel):
    id: int
    trip_id: int
    from_spot_id: Optional[int] = None
    to_spot_id: Optional[int] = None
    distance_km: Optional[float] = None
    duration_min: Optional[int] = None
    polyline: Optional[str] = None
    color: Optional[str] = None
    day_number: Optional[int] = None

    class Config:
        from_attributes = True
```

### 文件 3: backend/app/services/route_service.py
```python
import httpx
from app.config import settings

async def plan_route(from_lng: float, from_lat: float, to_lng: float, to_lat: float) -> dict:
    url = "https://restapi.amap.com/v3/direction/driving"
    params = {
        "origin": f"{from_lng},{from_lat}",
        "destination": f"{to_lng},{to_lat}",
        "strategy": 0,
        "extensions": "all",
        "key": settings.amap_key,
    }
    async with httpx.AsyncClient() as client:
        resp = await client.get(url, params=params)
        data = resp.json()
        if data.get("status") != "1":
            raise Exception(f"Amap API error: {data.get('info', 'unknown')}")
        path = data["route"]["paths"][0]
        polyline = ""
        for step in path["steps"]:
            polyline += step.get("polyline", "") + ";"
        polyline = polyline.rstrip(";")
        return {
            "distance_km": round(float(path["distance"]) / 1000, 2),
            "duration_min": round(int(path["duration"]) / 60),
            "polyline": polyline,
        }
```

### 文件 4: backend/app/routers/routes.py
```python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.deps import get_current_device_id
from app.models.route_segment import RouteSegment
from app.models.spot import Spot
from app.schemas.route_segment import RoutePlanRequest, RouteSegmentResponse
from app.services.route_service import plan_route

router = APIRouter(prefix="/api", tags=["routes"], dependencies=[Depends(get_current_device_id)])

@router.get("/trips/{trip_id}/routes", response_model=list[RouteSegmentResponse])
async def list_routes(trip_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(RouteSegment).where(RouteSegment.trip_id == trip_id).order_by(RouteSegment.day_number))
    segments = result.scalars().all()
    return [RouteSegmentResponse.model_validate(s) for s in segments]

@router.post("/trips/{trip_id}/routes/plan", response_model=RouteSegmentResponse, status_code=201)
async def plan(trip_id: int, data: RoutePlanRequest, db: AsyncSession = Depends(get_db)):
    from_result = await db.execute(select(Spot).where(Spot.id == data.from_spot_id))
    from_spot = from_result.scalar_one_or_none()
    to_result = await db.execute(select(Spot).where(Spot.id == data.to_spot_id))
    to_spot = to_result.scalar_one_or_none()
    if not from_spot or not to_spot:
        raise HTTPException(status_code=404, detail="Spot not found")
    try:
        result = await plan_route(float(from_spot.lng), float(from_spot.lat), float(to_spot.lng), float(to_spot.lat))
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e))
    segment = RouteSegment(
        trip_id=trip_id,
        from_spot_id=data.from_spot_id,
        to_spot_id=data.to_spot_id,
        distance_km=result["distance_km"],
        duration_min=result["duration_min"],
        polyline=result["polyline"],
        color=data.color,
        day_number=data.day_number,
    )
    db.add(segment)
    await db.commit()
    await db.refresh(segment)
    return RouteSegmentResponse.model_validate(segment)

@router.delete("/routes/{route_id}", status_code=204)
async def delete_route(route_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(RouteSegment).where(RouteSegment.id == route_id))
    segment = result.scalar_one_or_none()
    if not segment:
        raise HTTPException(status_code=404, detail="Route not found")
    await db.delete(segment)
    await db.commit()
```

### 文件 5: backend/app/main.py — 更新
Add `from app.routers.routes import router as route_router` and `app.include_router(route_router)`.

## Verification

```bash
cd /Users/mushroom/Documents/ai/hermes/projects/getaway_plan_v1/backend
for f in app/models/route_segment.py app/schemas/route_segment.py app/services/route_service.py app/routers/routes.py; do
  .venv/bin/python -c "import ast; ast.parse(open('$f').read())" && echo "✅ $f" || echo "❌ $f"
done
```