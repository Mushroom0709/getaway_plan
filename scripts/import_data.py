#!/usr/bin/env python3
"""
getaway_plan 数据导入脚本
从 qinggan-travel 项目导入数据，通过 REST API 写入
"""
import os
import json
import sys
import time
import requests
from urllib.parse import urljoin

API_BASE = os.environ.get("API_BASE", "http://localhost:10338/api/")
PASSWORD = os.environ.get("API_PASSWORD", "your_password")

def api(path, method="get", **kwargs):
    url = urljoin(API_BASE, path)
    headers = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}
    resp = requests.request(method, url, headers=headers, **kwargs)
    if resp.status_code >= 400:
        print(f"  ERROR {resp.status_code}: {resp.text[:200]}")
        return None
    return resp.json() if resp.text else None

def get_token():
    resp = requests.post(f"{API_BASE}auth/login", json={"password": PASSWORD})
    return resp.json()["token"]

# Login
print("🔑 登录...")
TOKEN = get_token()
print(f"   Token: {TOKEN[:50]}...")

# ========== 1. Load data ==========
print("\n📂 加载数据文件...")
with open("/tmp/spots.json") as f: spots_data = json.load(f)
with open("/tmp/hotels.json") as f: hotels_data = json.load(f)
with open("/tmp/food.json") as f: restaurants_data = json.load(f)
with open("/tmp/itinerary.json") as f: itinerary_data = json.load(f)
with open("/tmp/budget.json") as f: budget_data = json.load(f)
with open("/tmp/weather.json") as f: weather_data = json.load(f)
with open("/tmp/rental.json") as f: rental_data = json.load(f)
print(f"   Spots: {len(spots_data)}, Hotels: {sum(len(v) for v in hotels_data.values())}")
print(f"   Restaurants: {sum(len(v) for v in restaurants_data.values())}, Days: {len(itinerary_data)}")
print(f"   Budget: {len(budget_data)}, Weather: {len(weather_data)}, Cars: {len(rental_data)}")

# ========== 2. Create Trip ==========
print("\n📝 创建 Trip...")
trip = api("trips", "post", json={
    "name": "青甘大环线2026",
    "description": "8月下旬青甘大环线自驾游，武汉出发，自驾G227+连霍高速，7天6晚",
    "start_date": "2026-08-23",
    "end_date": "2026-08-29"
})
TRIP_ID = trip["id"]
print(f"   Trip ID: {TRIP_ID}")

# ========== 3. Create Days ==========
print("\n📅 创建 Days...")
day_map = {}  # day_number -> day_id
# itinerary is sorted: D0, D1, D2, ..., D6
for i, day_item in enumerate(itinerary_data):
    day_str = day_item["day"]  # "D0", "D1", ...
    day_num = int(day_str[1:])
    
    # Parse date
    base_date = "2026-08-23"
    if day_num == 0:
        day_date = base_date
    else:
        # Simple offset from base date
        day_date = f"2026-08-{23 + day_num}"
    
    day = api(f"trips/{TRIP_ID}/days", "post", json={
        "day_number": day_num,
        "date": day_date,
        "title": day_item["title"],
        "drive_hours": day_item["driveHours"],
        "hotel_city": day_item["hotelCity"],
        "sort_order": day_num
    })
    if day:
        day_map[day_num] = day["id"]
        print(f"   Day {day_num}: {day['title']} (ID={day['id']})")
    else:
        print(f"   Day {day_num}: FAILED!")

# ========== 4. Create Spots ==========
print("\n📍 创建 Spots...")
spot_map = {}  # qinggan_spot_id -> getaway_spot_id (for linking)

# Map qinggan day strings to gateway day_ids
qinggan_day_to_num = {"D0": 0, "D1": 1, "D2": 2, "D3": 3, "D4": 4, "D5": 5, "D6": 6}

# Category mapping
category_map = {
    "stay": "other",
    "scenic": "scenic",
    "photo": "photo",
}

for i, s in enumerate(spots_data):
    day_str = s.get("day", "D0")
    day_num = qinggan_day_to_num.get(day_str, 0)
    day_id = day_map.get(day_num)
    
    spot = api(f"trips/{TRIP_ID}/spots", "post", json={
        "day_id": day_id,
        "name": s["name"],
        "lng": s["lng"],
        "lat": s["lat"],
        "category": category_map.get(s["category"], "other"),
        "is_nav_point": True,
        "nav_order": i + 1,
        "description": s.get("description", ""),
        "intro": s.get("intro", "")
    })
    if spot:
        spot_map[s["id"]] = spot["id"]
        print(f"   [{i+1}/{len(spots_data)}] {s['name']} (ID={spot['id']})")
    else:
        print(f"   [{i+1}/{len(spots_data)}] {s['name']}: FAILED!")
    time.sleep(0.05)

# ========== 5. Create Attractions ==========
print("\n🏛️ 创建 Attractions...")
for s in spots_data:
    spot_id = spot_map.get(s["id"])
    if not spot_id:
        continue
    
    # Only for scenic/photo spots with extra info
    altitude = s.get("altitude")
    ticket = s.get("ticket")
    hours = s.get("hours")
    
    if not (altitude or ticket or hours):
        continue
    
    duration_hours = None
    if hours:
        try:
            # Parse "2-3h" or "1.5-2h" format
            parts = hours.replace("h", "").strip().split("-")
            if len(parts) == 2:
                duration_hours = (float(parts[0]) + float(parts[1])) / 2
            elif len(parts) == 1:
                duration_hours = float(parts[0])
        except:
            pass
    
    attr = api(f"spots/{spot_id}/attractions", "post", json={
        "ticket_price": ticket or "",
        "opening_hours": "全天",
        "best_time_of_day": "上午",
        "duration_hours": duration_hours,
        "altitude": altitude,
        "tips": s.get("intro", ""),
        "highlights": [],
        "must_see": False
    })
    if attr:
        print(f"   ✅ {s['name']}: altitude={altitude}, ticket={ticket}, hours={duration_hours}")
    else:
        print(f"   ❌ {s['name']}: FAILED")
    time.sleep(0.03)

# ========== 6. Create Hotels ==========
print("\n🏨 创建 Hotels...")
hotel_map = {}  # qinggan hotel id -> getaway hotel id

# Create hotel spots first, then hotel details
for city, city_hotels in hotels_data.items():
    for h in city_hotels:
        # Create hotel spot
        day_num = 0  # default
        # Match to the correct day based on city
        for d in itinerary_data:
            if d["hotelCity"] == city:
                day_num = qinggan_day_to_num.get(d["day"], 0)
                break
        
        day_id = day_map.get(day_num)
        
        spot = api(f"trips/{TRIP_ID}/spots", "post", json={
            "day_id": day_id,
            "name": h["name"],
            "lng": h["lng"],
            "lat": h["lat"],
            "category": "hotel",
            "is_nav_point": False,
            "description": f"宿{city}"
        })
        if not spot:
            print(f"   ❌ {h['name']} spot FAILED")
            continue
        
        # Create hotel detail
        hotel = api(f"trips/{TRIP_ID}/hotels", "post", json={
            "spot_id": spot["id"],
            "city": h["city"],
            "name": h["name"],
            "brand": h.get("brand", ""),
            "rating": h.get("rating"),
            "opened_year": h.get("openedYear"),
            "price_per_room": h.get("pricePerRoom"),
            "room_type": h.get("roomType", ""),
            "features": h.get("features", []),
            "lng": h["lng"],
            "lat": h["lat"],
            "notes": h.get("notes", "")
        })
        if hotel:
            hotel_map[h["id"]] = hotel["id"]
            print(f"   ✅ {h['name']} ({city}) hotel_id={hotel['id']}")
        else:
            print(f"   ❌ {h['name']} detail FAILED")
        time.sleep(0.05)

# ========== 7. Create Restaurants + Dishes ==========
print("\n🍽️ 创建 Restaurants...")
restaurant_id_map = {}  # qinggan restaurant id -> getaway restaurant id

for city, city_restaurants in restaurants_data.items():
    for r in city_restaurants:
        # Create restaurant spot
        day_num = 0
        for d in itinerary_data:
            if d["hotelCity"] == city:
                day_num = qinggan_day_to_num.get(d["day"], 0)
                break
        
        day_id = day_map.get(day_num)
        
        spot = api(f"trips/{TRIP_ID}/spots", "post", json={
            "day_id": day_id,
            "name": r["name"],
            "lng": r["lng"],
            "lat": r["lat"],
            "category": "restaurant",
            "is_nav_point": False,
            "description": f"{city}美食"
        })
        if not spot:
            print(f"   ❌ {r['name']} spot FAILED")
            continue
        
        # Create restaurant detail
        rest = api(f"trips/{TRIP_ID}/restaurants", "post", json={
            "spot_id": spot["id"],
            "city": r["city"],
            "name": r["name"],
            "address": r.get("address", ""),
            "lng": r["lng"],
            "lat": r["lat"],
            "rating": r.get("rating"),
            "avg_price": 60,
            "cuisine": "西北菜",
            "notes": ""
        })
        if not rest:
            print(f"   ❌ {r['name']} detail FAILED")
            continue
        
        rest_id = rest["id"]
        restaurant_id_map[r["id"]] = rest_id
        
        # Create dishes
        dish_count = 0
        for dish in r.get("dishes", []):
            d = api(f"restaurants/{rest_id}/dishs", "post", json={
                "name": dish["name"],
                "price": None,
                "description": dish.get("description", ""),
                "is_signature": True
            })
            if d:
                dish_count += 1
        
        print(f"   ✅ {r['name']} ({city}) rest_id={rest_id}, {dish_count} dishes")
        time.sleep(0.03)

# ========== 8. Create Budget ==========
print("\n💰 创建 Budget...")
for b in budget_data:
    item = api(f"trips/{TRIP_ID}/budget_items", "post", json={
        "category": "other",
        "item": b["item"],
        "unit_price": b.get("unitPrice", 0),
        "quantity": b.get("quantity", 1),
        "subtotal": b.get("subtotal", 0),
        "note": b.get("note", "")
    })
    if item:
        print(f"   ✅ {b['item'][:30]}...")
    time.sleep(0.03)
print(f"   Total: {len(budget_data)} items")

# ========== 9. Create Weather ==========
print("\n🌤️ 创建 Weather...")
for w in weather_data:
    item = api(f"trips/{TRIP_ID}/weathers", "post", json={
        "city": w["city"],
        "date": "2026-08-23",
        "high_temp": w.get("dayTemp", ""),
        "low_temp": w.get("nightTemp", ""),
        "weather_desc": "",
        "advice": w.get("advice", "")
    })
    if item:
        print(f"   ✅ {w['city']}")
    time.sleep(0.03)

# ========== 10. Create Rental Cars ==========
print("\n🚗 创建 Rental Cars...")
for c in rental_data:
    car = api(f"trips/{TRIP_ID}/cars", "post", json={
        "platform": c.get("platform", ""),
        "car_name": c["name"],
        "daily_price": c.get("dailyPrice"),
        "engine": c.get("engine", ""),
        "seats": c.get("seats"),
        "trunk": c.get("trunk", ""),
        "notes": c.get("notes", "")
    })
    if car:
        print(f"   ✅ {c['name']}")
    time.sleep(0.03)

# ========== 11. Create Social Notes ==========
print("\n📸 加载 Photos 数据...")
with open("/tmp/photos.json") as f:
    photos_data = json.load(f)

print(f"   Spots with photos: {len(photos_data)}")
total_notes = sum(len(v.get("groups", [])) for v in photos_data.values())
total_images = sum(
    len(g.get("photos", [])) 
    for v in photos_data.values()
    for g in v.get("groups", [])
)
print(f"   Total notes: {total_notes}, Total images: {total_images}")

print("\n📸 创建 Social Notes + Images (这需要一些时间)...")
note_count = 0
image_count = 0
errors = 0

for qg_spot_id, spot_photos in photos_data.items():
    gateway_spot_id = spot_map.get(qg_spot_id)
    if not gateway_spot_id:
        if qg_spot_id not in spot_map:
            print(f"   ⚠️  Spot '{qg_spot_id}' not found in spot_map, skipping {len(spot_photos.get('groups', []))} notes")
            continue
    
    for group in spot_photos.get("groups", []):
        photos = group.get("photos", [])
        if not photos:
            continue
        
        platform = group.get("platform", "").lower()
        if platform == "抖音":
            platform = "douyin"
        elif platform == "小红书":
            platform = "xiaohongshu"
        else:
            platform = "xiaohongshu"
        
        # Build images array
        images = []
        for idx, photo_path in enumerate(photos):
            # photo_path format: /photos/{spot_name}/{platform}/{author}/{filename}.jpeg
            images.append({
                "url": "",
                "url_large": "",
                "width": 0,
                "height": 0,
                "sort_order": idx,
                "local_path": photo_path
            })
        
        # Generate a unique note_id from the title
        import hashlib
        note_id = f"{qg_spot_id}_{group.get('author', 'unknown')}_{hashlib.md5(group.get('title', '').encode()).hexdigest()[:8]}"
        
        note = api(f"spots/{gateway_spot_id}/notes", "post", json={
            "platform": platform,
            "note_id": note_id,
            "title": group.get("title", "")[:500],
            "author": group.get("author", ""),
            "author_id": "",
            "likes": 0,
            "comments": 0,
            "shares": 0,
            "description": "",
            "source_url": "",
            "note_type": "normal",
            "images": images
        })
        if note:
            note_count += 1
            image_count += len(photos)
            if note_count % 50 == 0:
                print(f"   Progress: {note_count}/{total_notes} notes, {image_count} images")
        else:
            errors += 1
            if errors <= 3:
                print(f"   ❌ Failed: {group.get('author')} - {group.get('title', '')[:50]}")
        
        time.sleep(0.02)

print(f"\n✅ Social Notes: {note_count} notes, {image_count} images imported")
if errors:
    print(f"   ⚠️  {errors} errors")

print("\n" + "="*50)
print("🎉 数据导入完成!")
print(f"   Trip ID: {TRIP_ID}")
print(f"   Days: {len(day_map)}")
print(f"   Spots: {len(spot_map)}")
print(f"   Hotels: {len(hotel_map)}")
print(f"   Restaurants: {len(restaurant_id_map)}")
print(f"   Budget: {len(budget_data)}")
print(f"   Weather: {len(weather_data)}")
print(f"   Cars: {len(rental_data)}")
print(f"   Social Notes: {note_count} (total {total_notes} in source)")
print(f"   Social Images: {image_count} (total {total_images} in source)")
print(f"   Photos on disk: /opt/getaway_plan/photos/ (2.6GB, 21 dirs)")
print("="*50)
