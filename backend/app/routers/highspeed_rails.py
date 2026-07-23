from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.deps import get_current_device_id
from app.models.highspeed_rail import HighspeedRail
from app.schemas.highspeed_rail import HighspeedRailCreate, HighspeedRailUpdate, HighspeedRailResponse

router = APIRouter(prefix="/api", tags=["highspeed_rails"], dependencies=[Depends(get_current_device_id)])

@router.get("/trips/{trip_id}/rails", response_model=list[HighspeedRailResponse])
async def list_rails(trip_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(HighspeedRail).where(HighspeedRail.trip_id == trip_id).order_by(HighspeedRail.departure_time))
    rails = result.scalars().all()
    return [HighspeedRailResponse.model_validate(r) for r in rails]

@router.post("/trips/{trip_id}/rails", response_model=HighspeedRailResponse, status_code=201)
async def create_rail(trip_id: int, data: HighspeedRailCreate, db: AsyncSession = Depends(get_db)):
    rail = HighspeedRail(trip_id=trip_id, **data.model_dump())
    db.add(rail)
    await db.commit()
    await db.refresh(rail)
    return HighspeedRailResponse.model_validate(rail)

@router.put("/rails/{rail_id}", response_model=HighspeedRailResponse)
async def update_rail(rail_id: int, data: HighspeedRailUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(HighspeedRail).where(HighspeedRail.id == rail_id))
    rail = result.scalar_one_or_none()
    if not rail:
        raise HTTPException(status_code=404, detail="Rail not found")
    for key, val in data.model_dump(exclude_unset=True).items():
        setattr(rail, key, val)
    await db.commit()
    await db.refresh(rail)
    return HighspeedRailResponse.model_validate(rail)

@router.delete("/rails/{rail_id}", status_code=204)
async def delete_rail(rail_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(HighspeedRail).where(HighspeedRail.id == rail_id))
    rail = result.scalar_one_or_none()
    if not rail:
        raise HTTPException(status_code=404, detail="Rail not found")
    await db.delete(rail)
    await db.commit()
