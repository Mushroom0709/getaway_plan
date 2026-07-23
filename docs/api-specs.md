# API Specifications — getaway_plan

Base URL: `/api`
Auth: `Authorization: Bearer <JWT>` (除 /auth/login 外所有接口)

---

## 1. Auth

### POST /api/auth/login
```json
// Request
{ "password": "string" }
// Response 200
{ "token": "eyJ...", "expires_at": "2026-08-01T00:00:00Z" }
// Response 401
{ "detail": "Invalid password" }
```

### GET /api/auth/verify
```json
// Response 200
{ "valid": true, "expires_at": "2026-08-01T00:00:00Z" }
```

---

## 2. Trips

### GET /api/trips
```json
// Response 200
[{ "id": 1, "name": "青甘大环线", "start_date": "2026-08-23", "end_date": "2026-08-29", "status": "planning", "created_at": "..." }]
```

### POST /api/trips
```json
// Request
{ "name": "string", "description": "string?", "start_date": "2026-08-23", "end_date": "2026-08-29" }
// Response 201
{ "id": 1, "name": "...", ... }
```

### GET /api/trips/{id}
```json
// Response 200 (含嵌套数据)
{ "id": 1, "name": "...", "days": [...], "flights": [...], "budget_items": [...], ... }
```

### PUT /api/trips/{id}
```json
// Request (部分更新)
{ "name": "string?", "description": "string?", "status": "planning|active|completed" }
// Response 200
{ "id": 1, ... }
```

### DELETE /api/trips/{id}
```json
// Response 204
```

---

## 3. Days

### GET /api/trips/{trip_id}/days
```json
// Response 200
[{ "id": 1, "day_number": 0, "date": "2026-08-23", "title": "武汉 ✈ 西宁", "drive_hours": 0, "hotel_city": "西宁", "sort_order": 0 }]
```

### POST /api/trips/{trip_id}/days
```json
// Request
{ "day_number": 1, "date": "2026-08-24", "title": "西宁 → 祁连", "drive_hours": 4.5, "hotel_city": "祁连", "sort_order": 1 }
// Response 201
```

### PUT /api/days/{id}
```json
// Response 200
```

### DELETE /api/days/{id}
```json
// Response 204
```

---

## 4. Spots

### GET /api/trips/{trip_id}/spots
```json
// Query: ?day_id=1&category=scenic&is_nav_point=true
// Response 200
[{ "id": 1, "name": "岗什卡雪峰", "lng": 101.44, "lat": 37.69, "category": "scenic", "is_nav_point": true, "nav_order": 1, ... }]
```

### POST /api/trips/{trip_id}/spots
```json
// Request
{ "day_id": 1, "name": "string", "lng": 0.0, "lat": 0.0, "category": "scenic", "is_nav_point": false, "nav_order": null, "arrival_time": "14:00", "description": "string", "intro": "string" }
// Response 201
```

### PUT /api/spots/{id}
```json
// Response 200
```

### DELETE /api/spots/{id}
```json
// Response 204
```

### PUT /api/trips/{trip_id}/spots/reorder
```json
// 批量更新导航顺序
// Request
[{ "id": 1, "nav_order": 1 }, { "id": 2, "nav_order": 2 }]
// Response 200
```

---

## 5. Flights

### GET /api/trips/{trip_id}/flights
### POST /api/trips/{trip_id}/flights
### PUT /api/flights/{id}
### DELETE /api/flights/{id}

---

## 6. Highspeed Rails

### GET /api/trips/{trip_id}/rails
### POST /api/trips/{trip_id}/rails
### PUT /api/rails/{id}
### DELETE /api/rails/{id}

---

## 7. Rental Cars

### GET /api/trips/{trip_id}/cars
### POST /api/trips/{trip_id}/cars
### PUT /api/cars/{id}
### DELETE /api/cars/{id}

---

## 8. Route Segments

### GET /api/trips/{trip_id}/routes
```json
// Response 200
[{ "id": 1, "from_spot_id": 1, "to_spot_id": 2, "distance_km": 156.3, "duration_min": 150, "polyline": "...", "color": "#4caf50", "day_number": 1 }]
```

### POST /api/trips/{trip_id}/routes/plan
```json
// 调用高德 REST API 生成路线
// Request
{ "from_spot_id": 1, "to_spot_id": 2, "color": "#4caf50", "day_number": 1 }
// Response 201
{ "id": 1, "distance_km": 156.3, "duration_min": 150, "polyline": "lng1,lat1;lng2,lat2;...", ... }
```

### DELETE /api/routes/{id}
```json
// Response 204
```

---

## 9. Hotels

### GET /api/trips/{trip_id}/hotels
```json
// Query: ?city=西宁
// Response 200
```

### POST /api/trips/{trip_id}/hotels
```json
// Request
{ "spot_id": 1, "city": "西宁", "name": "亚朵酒店", "brand": "亚朵", "rating": 4.7, "opened_year": 2021, "price_per_room": 220, "room_type": "高级大床房", "features": ["阅读空间","自助洗衣"], "lng": 101.79, "lat": 36.62, "notes": "..." }
```

### PUT /api/hotels/{id}
### DELETE /api/hotels/{id}

---

## 10. Restaurants

### GET /api/trips/{trip_id}/restaurants
```json
// Query: ?city=西宁
```

### POST /api/trips/{trip_id}/restaurants
### PUT /api/restaurants/{id}
### DELETE /api/restaurants/{id}

---

## 11. Dishes

### GET /api/restaurants/{restaurant_id}/dishes
### POST /api/restaurants/{restaurant_id}/dishes
### PUT /api/dishes/{id}
### DELETE /api/dishes/{id}

---

## 12. Daily Meals

### GET /api/days/{day_id}/meals
### POST /api/days/{day_id}/meals
### DELETE /api/meals/{id}

---

## 13. Attractions

### GET /api/spots/{spot_id}/attraction
```json
// Response 200 (1:1)
{ "id": 1, "spot_id": 1, "ticket_price": "¥80", "opening_hours": "8:00-18:00", "best_time_of_day": "16:00-日落", "duration_hours": 2.5, "altitude": 4300, "tips": "...", "highlights": ["丹霞+草原+雪峰同框"], ... }
```

### POST /api/spots/{spot_id}/attraction
### PUT /api/attractions/{id}
### DELETE /api/attractions/{id}

---

## 14. Social Notes

### GET /api/spots/{spot_id}/notes
```json
// Query: ?platform=xiaohongshu
// Response 200
[{ "id": 1, "platform": "xiaohongshu", "note_id": "...", "title": "...", "author": "@xx", "likes": 236, "images": [...] }]
```

### POST /api/spots/{spot_id}/notes
```json
// Request
{ "platform": "xiaohongshu", "note_id": "xxx", "title": "...", "author": "@xx", "likes": 236, "description": "...", "images": [{ "url": "...", "url_large": "...", "width": 1440, "height": 1920, "sort_order": 0 }] }
```

### DELETE /api/notes/{id}

---

## 15. Social Images

### GET /api/notes/{note_id}/images
### DELETE /api/images/{id}

---

## 16. Budget Items

### GET /api/trips/{trip_id}/budget
### POST /api/trips/{trip_id}/budget
### PUT /api/budget/{id}
### DELETE /api/budget/{id}

---

## 17. Weather

### GET /api/trips/{trip_id}/weather
### POST /api/trips/{trip_id}/weather
### PUT /api/weather/{id}
### DELETE /api/weather/{id}

---

## 通用规范

### 错误响应格式
```json
{ "detail": "Error message" }
```

### HTTP 状态码
- 200: 成功
- 201: 创建成功
- 204: 删除成功（无返回体）
- 400: 请求参数错误
- 401: 未认证
- 404: 资源不存在
- 422: 数据校验失败
- 500: 服务器错误

### 分页（可选，后续实现）
```json
// Query: ?skip=0&limit=20
// Response
{ "items": [...], "total": 100, "skip": 0, "limit": 20 }
```

### 排序
所有 GET 列表接口支持 `?sort_by=created_at&order=desc`。