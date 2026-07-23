from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional
from app.database import get_db
from app.deps import get_current_device_id
from app.models.attraction import Attraction
from app.schemas.attraction import AttractionCreate, AttractionUpdate, AttractionResponse

router = APIRouter(prefix="/api", tags=["attraction"], dependencies=[Depends(get_current_device_id)])

@router.get("/spots/{spot_id}/attractions", response_model=list[AttractionResponse])
async def list_attractions(spot_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Attraction).where(Attraction.spot_id == spot_id))
    items = result.scalars().all()
    return [AttractionResponse.model_validate(x) for x in items]

@router.post("/spots/{spot_id}/attractions", response_model=AttractionResponse, status_code=201)
async def create_attraction(spot_id: int, data: AttractionCreate, db: AsyncSession = Depends(get_db)):
    item = Attraction(**data.model_dump())
    setattr(item, "spot_id", spot_id)
    db.add(item)
    await db.commit()
    await db.refresh(item)
    return AttractionResponse.model_validate(item)

@router.put("/attractions/{item_id}", response_model=AttractionResponse)
async def update_attraction(item_id: int, data: AttractionUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Attraction).where(Attraction.id == item_id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Not found")
    for key, val in data.model_dump(exclude_unset=True).items():
        setattr(item, key, val)
    await db.commit()
    await db.refresh(item)
    return AttractionResponse.model_validate(item)

@router.delete("/attractions/{item_id}", status_code=204)
async def delete_attraction(item_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Attraction).where(Attraction.id == item_id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Not found")
    await db.delete(item)
    await db.commit()
