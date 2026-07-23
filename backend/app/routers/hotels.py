from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional
from app.database import get_db
from app.deps import get_current_device_id
from app.models.hotel import Hotel
from app.schemas.hotel import HotelCreate, HotelUpdate, HotelResponse

router = APIRouter(prefix="/api", tags=["hotels"], dependencies=[Depends(get_current_device_id)])

@router.get("/trips/{trip_id}/hotels", response_model=list[HotelResponse])
async def list_hotels(
    trip_id: int,
    city: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db),
):
    stmt = select(Hotel).where(Hotel.trip_id == trip_id)
    if city is not None:
        stmt = stmt.where(Hotel.city == city)
    stmt = stmt.order_by(Hotel.id)
    result = await db.execute(stmt)
    hotels = result.scalars().all()
    return [HotelResponse.model_validate(h) for h in hotels]

@router.post("/trips/{trip_id}/hotels", response_model=HotelResponse, status_code=201)
async def create_hotel(trip_id: int, data: HotelCreate, db: AsyncSession = Depends(get_db)):
    hotel = Hotel(trip_id=trip_id, **data.model_dump())
    db.add(hotel)
    await db.commit()
    await db.refresh(hotel)
    return HotelResponse.model_validate(hotel)

@router.put("/hotels/{hotel_id}", response_model=HotelResponse)
async def update_hotel(hotel_id: int, data: HotelUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Hotel).where(Hotel.id == hotel_id))
    hotel = result.scalar_one_or_none()
    if not hotel:
        raise HTTPException(status_code=404, detail="Hotel not found")
    for key, val in data.model_dump(exclude_unset=True).items():
        setattr(hotel, key, val)
    await db.commit()
    await db.refresh(hotel)
    return HotelResponse.model_validate(hotel)

@router.delete("/hotels/{hotel_id}", status_code=204)
async def delete_hotel(hotel_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Hotel).where(Hotel.id == hotel_id))
    hotel = result.scalar_one_or_none()
    if not hotel:
        raise HTTPException(status_code=404, detail="Hotel not found")
    await db.delete(hotel)
    await db.commit()
