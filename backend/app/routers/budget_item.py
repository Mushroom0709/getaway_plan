from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional
from app.database import get_db
from app.deps import get_current_device_id
from app.models.budget_item import BudgetItem
from app.schemas.budget_item import BudgetItemCreate, BudgetItemUpdate, BudgetItemResponse

router = APIRouter(prefix="/api", tags=["budget_item"], dependencies=[Depends(get_current_device_id)])

@router.get("/trips/{trip_id}/budget_items", response_model=list[BudgetItemResponse])
async def list_budget_items(trip_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(BudgetItem).where(BudgetItem.trip_id == trip_id))
    items = result.scalars().all()
    return [BudgetItemResponse.model_validate(x) for x in items]

@router.post("/trips/{trip_id}/budget_items", response_model=BudgetItemResponse, status_code=201)
async def create_budget_item(trip_id: int, data: BudgetItemCreate, db: AsyncSession = Depends(get_db)):
    item = BudgetItem(**data.model_dump())
    setattr(item, "trip_id", trip_id)
    db.add(item)
    await db.commit()
    await db.refresh(item)
    return BudgetItemResponse.model_validate(item)

@router.put("/budget_items/{item_id}", response_model=BudgetItemResponse)
async def update_budget_item(item_id: int, data: BudgetItemUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(BudgetItem).where(BudgetItem.id == item_id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Not found")
    for key, val in data.model_dump(exclude_unset=True).items():
        setattr(item, key, val)
    await db.commit()
    await db.refresh(item)
    return BudgetItemResponse.model_validate(item)

@router.delete("/budget_items/{item_id}", status_code=204)
async def delete_budget_item(item_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(BudgetItem).where(BudgetItem.id == item_id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Not found")
    await db.delete(item)
    await db.commit()
