from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers.auth import router as auth_router
from app.routers.trips import router as trip_router
from app.routers.days import router as day_router
from app.routers.spots import router as spot_router
from app.routers.routes import router as route_router
from app.routers.flights import router as flight_router
from app.routers.highspeed_rails import router as rail_router
from app.routers.rental_cars import router as car_router
from app.routers.hotels import router as hotel_router
from app.routers.restaurant import router as restaurant_router
from app.routers.dish import router as dish_router
from app.routers.daily_meal import router as meal_router
from app.routers.attraction import router as attraction_router
from app.routers.social_note import router as note_router
from app.routers.social_image import router as image_router
from app.routers.budget_item import router as budget_router
from app.routers.weather import router as weather_router

app = FastAPI(title="Getaway Plan API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(trip_router)
app.include_router(day_router)
app.include_router(spot_router)
app.include_router(route_router)
app.include_router(flight_router)
app.include_router(rail_router)
app.include_router(car_router)
app.include_router(hotel_router)
app.include_router(restaurant_router)
app.include_router(dish_router)
app.include_router(meal_router)
app.include_router(attraction_router)
app.include_router(note_router)
app.include_router(image_router)
app.include_router(budget_router)
app.include_router(weather_router)

@app.get("/api/health")
async def health():
    return {"status": "ok"}
