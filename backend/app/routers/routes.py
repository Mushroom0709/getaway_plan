from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.deps import get_current_device_id
from app.models.route_segment import RouteSegment
from app.models.spot import Spot
from app.schemas.route_segment import RoutePlanRequest, RouteCreateRequest, RouteSegmentResponse
from app.services.route_service import plan_route

router = APIRouter(prefix="/api", tags=["routes"], dependencies=[Depends(get_current_device_id)])

@router.get("/trips/{trip_id}/routes", response_model=list[RouteSegmentResponse])
async def list_routes(trip_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(RouteSegment).where(RouteSegment.trip_id == trip_id).order_by(RouteSegment.day_number))
    segments = result.scalars().all()
    return [RouteSegmentResponse.model_validate(s) for s in segments]

@router.post("/trips/{trip_id}/routes/plan", response_model=RouteSegmentResponse, status_code=201)
async def plan(trip_id: int, data: RoutePlanRequest, db: AsyncSession = Depends(get_db)):
    from_result = await db.execute(select(Spot).where(Spot.id == data.from_spot_id))
    from_spot = from_result.scalar_one_or_none()
    to_result = await db.execute(select(Spot).where(Spot.id == data.to_spot_id))
    to_spot = to_result.scalar_one_or_none()
    if not from_spot or not to_spot:
        raise HTTPException(status_code=404, detail="Spot not found")
    try:
        result = await plan_route(float(from_spot.lng), float(from_spot.lat), float(to_spot.lng), float(to_spot.lat))
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e))
    segment = RouteSegment(
        trip_id=trip_id,
        from_spot_id=data.from_spot_id,
        to_spot_id=data.to_spot_id,
        distance_km=result["distance_km"],
        duration_min=result["duration_min"],
        polyline=result["polyline"],
        color=data.color,
        day_number=data.day_number,
        route_type=data.route_type,
    )
    db.add(segment)
    await db.commit()
    await db.refresh(segment)
    return RouteSegmentResponse.model_validate(segment)

@router.post("/trips/{trip_id}/routes", response_model=RouteSegmentResponse, status_code=201)
async def create_route(trip_id: int, data: RouteCreateRequest, db: AsyncSession = Depends(get_db)):
    """Create a route segment directly (for transit/conceptual routes without driving API)"""
    segment = RouteSegment(
        trip_id=trip_id,
        from_spot_id=data.from_spot_id,
        to_spot_id=data.to_spot_id,
        distance_km=data.distance_km,
        duration_min=data.duration_min,
        polyline=data.polyline,
        color=data.color,
        day_number=data.day_number,
        route_type=data.route_type,
    )
    db.add(segment)
    await db.commit()
    await db.refresh(segment)
    return RouteSegmentResponse.model_validate(segment)

@router.delete("/routes/{route_id}", status_code=204)
async def delete_route(route_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(RouteSegment).where(RouteSegment.id == route_id))
    segment = result.scalar_one_or_none()
    if not segment:
        raise HTTPException(status_code=404, detail="Route not found")
    await db.delete(segment)
    await db.commit()
