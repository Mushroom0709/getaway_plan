from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional
from app.database import get_db
from app.deps import get_current_device_id
from app.models.restaurant import Restaurant
from app.schemas.restaurant import RestaurantCreate, RestaurantUpdate, RestaurantResponse

router = APIRouter(prefix="/api", tags=["restaurant"], dependencies=[Depends(get_current_device_id)])

@router.get("/trips/{trip_id}/restaurants", response_model=list[RestaurantResponse])
async def list_restaurants(trip_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Restaurant).where(Restaurant.trip_id == trip_id))
    items = result.scalars().all()
    return [RestaurantResponse.model_validate(x) for x in items]

@router.post("/trips/{trip_id}/restaurants", response_model=RestaurantResponse, status_code=201)
async def create_restaurant(trip_id: int, data: RestaurantCreate, db: AsyncSession = Depends(get_db)):
    item = Restaurant(**data.model_dump())
    setattr(item, "trip_id", trip_id)
    db.add(item)
    await db.commit()
    await db.refresh(item)
    return RestaurantResponse.model_validate(item)

@router.put("/restaurants/{item_id}", response_model=RestaurantResponse)
async def update_restaurant(item_id: int, data: RestaurantUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Restaurant).where(Restaurant.id == item_id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Not found")
    for key, val in data.model_dump(exclude_unset=True).items():
        setattr(item, key, val)
    await db.commit()
    await db.refresh(item)
    return RestaurantResponse.model_validate(item)

@router.delete("/restaurants/{item_id}", status_code=204)
async def delete_restaurant(item_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Restaurant).where(Restaurant.id == item_id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Not found")
    await db.delete(item)
    await db.commit()
