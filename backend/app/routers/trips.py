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
