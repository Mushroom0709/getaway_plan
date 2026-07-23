from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.deps import get_current_device_id
from app.models.flight import Flight
from app.schemas.flight import FlightCreate, FlightUpdate, FlightResponse

router = APIRouter(prefix="/api", tags=["flights"], dependencies=[Depends(get_current_device_id)])

@router.get("/trips/{trip_id}/flights", response_model=list[FlightResponse])
async def list_flights(trip_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Flight).where(Flight.trip_id == trip_id).order_by(Flight.departure_time))
    flights = result.scalars().all()
    return [FlightResponse.model_validate(f) for f in flights]

@router.post("/trips/{trip_id}/flights", response_model=FlightResponse, status_code=201)
async def create_flight(trip_id: int, data: FlightCreate, db: AsyncSession = Depends(get_db)):
    flight = Flight(trip_id=trip_id, **data.model_dump())
    db.add(flight)
    await db.commit()
    await db.refresh(flight)
    return FlightResponse.model_validate(flight)

@router.put("/flights/{flight_id}", response_model=FlightResponse)
async def update_flight(flight_id: int, data: FlightUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Flight).where(Flight.id == flight_id))
    flight = result.scalar_one_or_none()
    if not flight:
        raise HTTPException(status_code=404, detail="Flight not found")
    for key, val in data.model_dump(exclude_unset=True).items():
        setattr(flight, key, val)
    await db.commit()
    await db.refresh(flight)
    return FlightResponse.model_validate(flight)

@router.delete("/flights/{flight_id}", status_code=204)
async def delete_flight(flight_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Flight).where(Flight.id == flight_id))
    flight = result.scalar_one_or_none()
    if not flight:
        raise HTTPException(status_code=404, detail="Flight not found")
    await db.delete(flight)
    await db.commit()
