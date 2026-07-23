import httpx
from app.config import settings

async def plan_route(from_lng: float, from_lat: float, to_lng: float, to_lat: float) -> dict:
    url = "https://restapi.amap.com/v3/direction/driving"
    params = {
        "origin": f"{from_lng},{from_lat}",
        "destination": f"{to_lng},{to_lat}",
        "strategy": 0,
        "extensions": "all",
        "key": settings.amap_key,
    }
    async with httpx.AsyncClient() as client:
        resp = await client.get(url, params=params)
        data = resp.json()
        if data.get("status") != "1":
            raise Exception(f"Amap API error: {data.get('info', 'unknown')}")
        path = data["route"]["paths"][0]
        polyline = ""
        for step in path["steps"]:
            polyline += step.get("polyline", "") + ";"
        polyline = polyline.rstrip(";")
        return {
            "distance_km": round(float(path["distance"]) / 1000, 2),
            "duration_min": round(int(path["duration"]) / 60),
            "polyline": polyline,
        }
