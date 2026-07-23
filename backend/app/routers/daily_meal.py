from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional
from app.database import get_db
from app.deps import get_current_device_id
from app.models.daily_meal import DailyMeal
from app.schemas.daily_meal import DailyMealCreate, DailyMealResponse

router = APIRouter(prefix="/api", tags=["daily_meal"], dependencies=[Depends(get_current_device_id)])

@router.get("/days/{day_id}/daily_meals", response_model=list[DailyMealResponse])
async def list_daily_meals(day_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(DailyMeal).where(DailyMeal.day_id == day_id))
    items = result.scalars().all()
    return [DailyMealResponse.model_validate(x) for x in items]

@router.post("/days/{day_id}/daily_meals", response_model=DailyMealResponse, status_code=201)
async def create_daily_meal(day_id: int, data: DailyMealCreate, db: AsyncSession = Depends(get_db)):
    item = DailyMeal(**data.model_dump())
    setattr(item, "day_id", day_id)
    db.add(item)
    await db.commit()
    await db.refresh(item)
    return DailyMealResponse.model_validate(item)

@router.delete("/daily_meals/{item_id}", status_code=204)
async def delete_daily_meal(item_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(DailyMeal).where(DailyMeal.id == item_id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Not found")
    await db.delete(item)
    await db.commit()
