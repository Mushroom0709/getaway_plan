from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional
from app.database import get_db
from app.deps import get_current_device_id
from app.models.weather import Weather
from app.schemas.weather import WeatherCreate, WeatherUpdate, WeatherResponse

router = APIRouter(prefix="/api", tags=["weather"], dependencies=[Depends(get_current_device_id)])

@router.get("/trips/{trip_id}/weathers", response_model=list[WeatherResponse])
async def list_weathers(trip_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Weather).where(Weather.trip_id == trip_id))
    items = result.scalars().all()
    return [WeatherResponse.model_validate(x) for x in items]

@router.post("/trips/{trip_id}/weathers", response_model=WeatherResponse, status_code=201)
async def create_weather(trip_id: int, data: WeatherCreate, db: AsyncSession = Depends(get_db)):
    item = Weather(**data.model_dump())
    setattr(item, "trip_id", trip_id)
    db.add(item)
    await db.commit()
    await db.refresh(item)
    return WeatherResponse.model_validate(item)

@router.put("/weathers/{item_id}", response_model=WeatherResponse)
async def update_weather(item_id: int, data: WeatherUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Weather).where(Weather.id == item_id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Not found")
    for key, val in data.model_dump(exclude_unset=True).items():
        setattr(item, key, val)
    await db.commit()
    await db.refresh(item)
    return WeatherResponse.model_validate(item)

@router.delete("/weathers/{item_id}", status_code=204)
async def delete_weather(item_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Weather).where(Weather.id == item_id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Not found")
    await db.delete(item)
    await db.commit()
