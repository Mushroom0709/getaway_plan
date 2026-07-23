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
