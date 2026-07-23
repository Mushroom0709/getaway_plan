from pydantic import BaseModel
from typing import Optional

class RoutePlanRequest(BaseModel):
    from_spot_id: int
    to_spot_id: int
    color: str = "#4caf50"
    day_number: Optional[int] = None
    route_type: str = "driving"  # "driving" or "transit"

class RouteCreateRequest(BaseModel):
    from_spot_id: int
    to_spot_id: int
    color: str = "#4caf50"
    day_number: Optional[int] = None
    route_type: str = "transit"
    distance_km: Optional[float] = None
    duration_min: Optional[int] = None
    polyline: Optional[str] = None

class RouteSegmentResponse(BaseModel):
    id: int
    trip_id: int
    from_spot_id: Optional[int] = None
    to_spot_id: Optional[int] = None
    distance_km: Optional[float] = None
    duration_min: Optional[int] = None
    polyline: Optional[str] = None
    color: Optional[str] = None
    day_number: Optional[int] = None
    route_type: Optional[str] = "driving"

    class Config:
        from_attributes = True
