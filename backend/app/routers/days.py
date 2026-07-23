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
