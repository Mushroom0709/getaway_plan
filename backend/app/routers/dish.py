from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional
from app.database import get_db
from app.deps import get_current_device_id
from app.models.dish import Dish
from app.schemas.dish import DishCreate, DishUpdate, DishResponse

router = APIRouter(prefix="/api", tags=["dish"], dependencies=[Depends(get_current_device_id)])

@router.get("/restaurants/{restaurant_id}/dishs", response_model=list[DishResponse])
async def list_dishs(restaurant_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Dish).where(Dish.restaurant_id == restaurant_id))
    items = result.scalars().all()
    return [DishResponse.model_validate(x) for x in items]

@router.post("/restaurants/{restaurant_id}/dishs", response_model=DishResponse, status_code=201)
async def create_dish(restaurant_id: int, data: DishCreate, db: AsyncSession = Depends(get_db)):
    item = Dish(**data.model_dump())
    setattr(item, "restaurant_id", restaurant_id)
    db.add(item)
    await db.commit()
    await db.refresh(item)
    return DishResponse.model_validate(item)

@router.put("/dishs/{item_id}", response_model=DishResponse)
async def update_dish(item_id: int, data: DishUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Dish).where(Dish.id == item_id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Not found")
    for key, val in data.model_dump(exclude_unset=True).items():
        setattr(item, key, val)
    await db.commit()
    await db.refresh(item)
    return DishResponse.model_validate(item)

@router.delete("/dishs/{item_id}", status_code=204)
async def delete_dish(item_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Dish).where(Dish.id == item_id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Not found")
    await db.delete(item)
    await db.commit()
