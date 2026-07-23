# S7-S10: Hotels + Restaurants + Dishes + Meals + Attractions + Notes + Budget + Weather

## Goal

一次性实现剩余的 8 个 CRUD 模块：hotels, restaurants, dishes, daily_meals, attractions, social_notes, social_images, budget_items, weather。

## Acceptance Criteria

- [ ] Hotels CRUD: POST/GET /api/trips/{trip_id}/hotels + PUT/DELETE /api/hotels/{id}
- [ ] Restaurants CRUD: POST/GET /api/trips/{trip_id}/restaurants + PUT/DELETE /api/restaurants/{id}
- [ ] Dishes CRUD: POST/GET /api/restaurants/{restaurant_id}/dishes + PUT/DELETE /api/dishes/{id}
- [ ] Daily Meals: POST/GET /api/days/{day_id}/meals + DELETE /api/meals/{id}
- [ ] Attractions CRUD: POST/GET /api/spots/{spot_id}/attraction + PUT/DELETE /api/attractions/{id}
- [ ] Social Notes: POST /api/spots/{spot_id}/notes (级联创建 images) + GET + DELETE
- [ ] Social Images: GET /api/notes/{note_id}/images + DELETE
- [ ] Budget Items CRUD: POST/GET /api/trips/{trip_id}/budget + PUT/DELETE /api/budget/{id}
- [ ] Weather CRUD: POST/GET /api/trips/{trip_id}/weather + PUT/DELETE /api/weather/{id}

## Recipe

All models extend `app.models.trip.Base`. Standard CRUD pattern same as previous slices. For social_notes, POST must create child social_images in one transaction.

### Models (one file each, under backend/app/models/):

hotel.py: columns id, trip_id(FK), spot_id(FK nullable), city, name, brand, rating(Numeric 2,1), opened_year, price_per_room, room_type, features(JSON), check_in_date, check_out_date, lng, lat, phone, cover_image, notes

restaurant.py: columns id, trip_id(FK), spot_id(FK nullable), city, name, address, lng, lat, rating, avg_price, cuisine, phone, opening_hours, maps_url, cover_image, notes

dish.py: columns id, restaurant_id(FK), name, price, description, image, is_signature(Boolean)

daily_meal.py: columns id, day_id(FK), restaurant_id(FK), meal_type(Enum: breakfast/lunch/dinner/snack), notes

attraction.py: columns id, spot_id(FK unique), ticket_price, opening_hours, best_season, best_time_of_day, duration_hours, altitude, tips, highlights(JSON), must_see(Boolean)

social_note.py: columns id, spot_id(FK), platform(Enum: xiaohongshu/douyin), note_id, title, author, author_id, likes, comments, shares, description, xsec_token, source_url, note_type, fetched_at

social_image.py: columns id, note_id(FK), url, url_large, width, height, sort_order, local_path

budget_item.py: columns id, trip_id(FK), category(Enum: flight/hotel/car/food/ticket/rail/other), item, unit_price, quantity, subtotal, note

weather.py: columns id, trip_id(FK), city, date, high_temp, low_temp, weather_desc, advice

### Schemas + Routers:
Standard Create/Update/Response schemas for each model. All routers follow pattern from S3/S4.

### main.py update:
Import and include_router for all new routers.

## Verification

```bash
cd /Users/mushroom/Documents/ai/hermes/projects/getaway_plan_v1/backend
for f in app/models/hotel.py app/models/restaurant.py app/models/dish.py app/models/daily_meal.py app/models/attraction.py app/models/social_note.py app/models/social_image.py app/models/budget_item.py app/models/weather.py; do
  .venv/bin/python -c "import ast; ast.parse(open('$f').read())" && echo "✅ $f" || echo "❌ $f"
done
```