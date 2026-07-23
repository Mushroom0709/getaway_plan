# AI Agent API Guide — getaway_plan

> 本文档写给使用者的 AI Agent，用于通过标准 API 接口操作旅行规划数据。

## 快速开始

### 1. 认证
```bash
# 获取 token（密码由用户提供）
curl -X POST http://HOST:10338/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"password": "YOUR_PASSWORD"}'

# 返回 {"token": "eyJ...", "expires_at": "..."}
# 后续所有请求带上: Authorization: Bearer <token>
```

### 2. 数据层级
```
Trip (旅行计划)
 ├── Day (每天行程)
 │   ├── Spot (坐标点: 景区/拍照点/酒店/餐厅/机场/高铁站)
 │   │   ├── Attraction (景点详情)
 │   │   ├── Hotel (酒店详情)
 │   │   ├── Restaurant (餐厅详情)
 │   │   │   └── Dish (菜品)
 │   │   └── SocialNote (小红书/抖音笔记)
 │   │       └── SocialImage (笔记图片)
 │   └── DailyMeal (每日饮食安排)
 ├── Flight (航班)
 ├── HighspeedRail (高铁)
 ├── RentalCar (租车)
 ├── RouteSegment (导航路段)
 ├── BudgetItem (费用)
 └── Weather (天气)
```

## 典型场景

### 场景 1: 创建一个新旅行计划

```bash
# 步骤 1: 创建 trip
curl -X POST http://HOST:10338/api/trips \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "青甘大环线2026",
    "description": "8月下旬青甘大环线自驾游",
    "start_date": "2026-08-23",
    "end_date": "2026-08-29"
  }'

# 返回 {"id": 1, ...}
# 记住 trip_id = 1
```

### 场景 2: 添加每日行程

```bash
# 步骤 2: 创建 day
TRIP_ID=1
curl -X POST http://HOST:10338/api/trips/$TRIP_ID/days \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "day_number": 1,
    "date": "2026-08-24",
    "title": "西宁 → 祁连",
    "drive_hours": 4.5,
    "hotel_city": "祁连",
    "sort_order": 1
  }'
# 返回 {"id": 10, ...}
```

### 场景 3: 添加坐标点（景点/拍照点/酒店/机场）

```bash
# 步骤 3: 添加景点坐标
DAY_ID=10
curl -X POST http://HOST:10338/api/trips/$TRIP_ID/spots \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "day_id": '$DAY_ID',
    "name": "岗什卡雪峰",
    "lng": 101.44,
    "lat": 37.69,
    "category": "scenic",
    "is_nav_point": true,
    "nav_order": 2,
    "arrival_time": "13:30",
    "description": "5254m·免费雪山·连心湖",
    "intro": "祁连山脉东段最高峰，海拔5254.5m..."
  }'
# 返回 {"id": 100, ...}
```

### 场景 4: 添加景点详情

```bash
# 步骤 4: 关联景点详情
SPOT_ID=100
curl -X POST http://HOST:10338/api/spots/$SPOT_ID/attraction \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "ticket_price": "免费",
    "opening_hours": "全天",
    "best_time_of_day": "上午",
    "duration_hours": 1.5,
    "altitude": 5254,
    "tips": "清晨或黄昏光线最佳，广角镜头收入丹霞+草原+雪山三元素",
    "highlights": ["5254m雪山", "连心湖翠绿湖水", "免费开放"],
    "must_see": true
  }'
```

### 场景 5: 添加酒店

```bash
# 步骤 5: 添加酒店（先添加 spot 类型的坐标点，再关联酒店详情）
# 先创建酒店坐标点
curl -X POST http://HOST:10338/api/trips/$TRIP_ID/spots \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "day_id": '$DAY_ID',
    "name": "祁连吉缘饭店",
    "lng": 100.25,
    "lat": 38.18,
    "category": "hotel",
    "is_nav_point": false,
    "description": "D1 宿祁连县"
  }'
# 返回 {"id": 101, ...}

# 再关联酒店详情
curl -X POST http://HOST:10338/api/trips/$TRIP_ID/hotels \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "spot_id": 101,
    "city": "祁连",
    "name": "祁连吉缘饭店",
    "brand": "本地精品",
    "rating": 4.8,
    "opened_year": 2022,
    "price_per_room": 220,
    "room_type": "家庭房",
    "features": ["24h弥漫供氧", "卓尔山双景", "亲子友好"],
    "lng": 100.25,
    "lat": 38.18,
    "notes": "祁连口碑最佳，供氧是刚需"
  }'
```

### 场景 6: 添加餐厅和菜品

```bash
# 步骤 6: 添加餐厅（先坐标点，再餐厅详情，再菜品）
# 创建餐厅坐标点
curl -X POST http://HOST:10338/api/trips/$TRIP_ID/spots \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "day_id": '$DAY_ID',
    "name": "马忠食府",
    "lng": 101.78,
    "lat": 36.62,
    "category": "restaurant",
    "is_nav_point": false,
    "description": "西宁特色美食"
  }'
# 返回 {"id": 102, ...}

# 创建餐厅详情
curl -X POST http://HOST:10338/api/trips/$TRIP_ID/restaurants \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "spot_id": 102,
    "city": "西宁",
    "name": "马忠食府（莫家街店）",
    "address": "西宁市城中区莫家街",
    "lng": 101.78,
    "lat": 36.62,
    "rating": 4.6,
    "avg_price": 60,
    "cuisine": "西北菜",
    "notes": "青海招牌美食集中地"
  }'
# 返回 {"id": 200, ...}

# 添加菜品
RESTAURANT_ID=200
curl -X POST http://HOST:10338/api/restaurants/$RESTAURANT_ID/dishes \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "手抓羊肉",
    "price": 88,
    "description": "青海招牌，白水煮羊肉蘸椒盐",
    "is_signature": true
  }'
```

### 场景 7: 添加小红书/抖音笔记

```bash
# 步骤 7: 添加社交媒体笔记
SPOT_ID=100
curl -X POST http://HOST:10338/api/spots/$SPOT_ID/notes \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "platform": "xiaohongshu",
    "note_id": "abc123",
    "title": "岗什卡雪峰绝美！",
    "author": "@旅行达人",
    "author_id": "user_001",
    "likes": 236,
    "comments": 15,
    "shares": 42,
    "description": "8月的岗什卡雪峰...",
    "source_url": "https://www.xiaohongshu.com/explore/abc123",
    "note_type": "normal",
    "images": [
      {
        "url": "https://ci.xiaohongshu.com/xxx.jpg",
        "url_large": "https://ci.xiaohongshu.com/xxx.jpg?imageView2/2/w/2880",
        "width": 1440,
        "height": 1920,
        "sort_order": 0
      }
    ]
  }'
```

### 场景 8: 生成路线（导航路段）

```bash
# 步骤 8: 调用高德 API 生成实际道路路线
FROM_SPOT=1   # 西宁
TO_SPOT=100   # 岗什卡雪峰
curl -X POST http://HOST:10338/api/trips/$TRIP_ID/routes/plan \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "from_spot_id": '$FROM_SPOT',
    "to_spot_id": '$TO_SPOT',
    "color": "#4caf50",
    "day_number": 1
  }'
# 返回 { "id": 1, "distance_km": 156.3, "duration_min": 150, "polyline": "..." }
```

### 场景 9: 添加航班/高铁

```bash
# 添加航班
curl -X POST http://HOST:10338/api/trips/$TRIP_ID/flights \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "flight_no": "MU6631",
    "airline": "东方航空",
    "departure_city": "武汉",
    "departure_airport": "武汉天河",
    "arrival_city": "西宁",
    "arrival_airport": "西宁曹家堡",
    "departure_time": "2026-08-23T09:55:00",
    "arrival_time": "2026-08-23T12:20:00",
    "duration_min": 145,
    "price": 800,
    "seat_class": "经济舱"
  }'

# 添加高铁
curl -X POST http://HOST:10338/api/trips/$TRIP_ID/rails \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "train_no": "G2026",
    "departure_city": "兰州",
    "departure_station": "兰州西站",
    "arrival_city": "西宁",
    "arrival_station": "西宁站",
    "departure_time": "2026-08-23T14:00:00",
    "arrival_time": "2026-08-23T15:30:00",
    "duration_min": 90,
    "price": 58,
    "seat_class": "二等座"
  }'
```

### 场景 10: 添加费用

```bash
curl -X POST http://HOST:10338/api/trips/$TRIP_ID/budget \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "category": "flight",
    "item": "武汉→西宁机票",
    "unit_price": 800,
    "quantity": 3,
    "subtotal": 2400,
    "note": "人均¥800，8月下旬参考价"
  }'
```

## 数据规范

### Spot category 枚举
| 值 | 含义 | 前端展示 |
|----|------|---------|
| airport | 机场 | ✈ |
| highspeed_rail | 高铁站 | 🚄 |
| train | 火车站 | 🚂 |
| scenic | 核心景区 | ⭐ 大图标 |
| photo | 拍照打卡点 | 📸 小图标 |
| hotel | 酒店 | 🏠 |
| restaurant | 餐厅 | 🍴 |
| other | 其他 | ● |

### 导航规则
- `is_nav_point=true` 的点参与路线规划
- 按 `nav_order` 升序连接
- 高德 REST API 逐段计算实际道路
- 前端 `AMap.Polyline(showDir: true)` 显示方向箭头

### 图片存储
- 小红书/抖音图片下载后存储到服务器 `/opt/photos/{spot_name}/{platform}/{author}/`
- `social_images.local_path` 存储服务器本地路径
- 前端通过 `/photos/...` 访问

## 调用顺序建议

AI Agent 规划旅行时的推荐调用顺序：

1. `POST /api/auth/login` → 获取 token
2. `POST /api/trips` → 创建旅行
3. `POST /api/trips/{id}/days` → 逐天创建行程
4. `POST /api/trips/{id}/spots` → 添加坐标点（含导航点标记）
5. `POST /api/spots/{id}/attraction` → 关联景点详情
6. `POST /api/trips/{id}/hotels` → 关联酒店
7. `POST /api/trips/{id}/restaurants` → 关联餐厅
8. `POST /api/restaurants/{id}/dishes` → 添加菜品
9. `POST /api/spots/{id}/notes` → 添加小红书/抖音笔记
10. `POST /api/trips/{id}/routes/plan` → 逐段生成路线
11. `POST /api/trips/{id}/flights` → 添加航班
12. `POST /api/trips/{id}/rails` → 添加高铁
13. `POST /api/trips/{id}/cars` → 添加租车
14. `POST /api/trips/{id}/budget` → 添加费用
15. `POST /api/trips/{id}/weather` → 添加天气