from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.deps import get_current_device_id
from app.models.rental_car import RentalCar
from app.schemas.rental_car import RentalCarCreate, RentalCarUpdate, RentalCarResponse

router = APIRouter(prefix="/api", tags=["rental_cars"], dependencies=[Depends(get_current_device_id)])

@router.get("/trips/{trip_id}/cars", response_model=list[RentalCarResponse])
async def list_cars(trip_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(RentalCar).where(RentalCar.trip_id == trip_id).order_by(RentalCar.id))
    cars = result.scalars().all()
    return [RentalCarResponse.model_validate(c) for c in cars]

@router.post("/trips/{trip_id}/cars", response_model=RentalCarResponse, status_code=201)
async def create_car(trip_id: int, data: RentalCarCreate, db: AsyncSession = Depends(get_db)):
    car = RentalCar(trip_id=trip_id, **data.model_dump())
    db.add(car)
    await db.commit()
    await db.refresh(car)
    return RentalCarResponse.model_validate(car)

@router.put("/cars/{car_id}", response_model=RentalCarResponse)
async def update_car(car_id: int, data: RentalCarUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(RentalCar).where(RentalCar.id == car_id))
    car = result.scalar_one_or_none()
    if not car:
        raise HTTPException(status_code=404, detail="Car not found")
    for key, val in data.model_dump(exclude_unset=True).items():
        setattr(car, key, val)
    await db.commit()
    await db.refresh(car)
    return RentalCarResponse.model_validate(car)

@router.delete("/cars/{car_id}", status_code=204)
async def delete_car(car_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(RentalCar).where(RentalCar.id == car_id))
    car = result.scalar_one_or_none()
    if not car:
        raise HTTPException(status_code=404, detail="Car not found")
    await db.delete(car)
    await db.commit()
