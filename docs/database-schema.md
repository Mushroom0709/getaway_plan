# Database Schema — getaway_plan

## 表关系图

```
trips ──1:N──> days ──1:N──> spots ──1:N──> attractions
  │                │              │──1:N──> social_notes ──1:N──> social_images
  │                │              │──1:N──> hotels
  │                │              │──1:N──> restaurants ──1:N──> dishes
  │                │              │──1:N──> daily_meals
  │                │
  │──1:N──> flights
  │──1:N──> highspeed_rails
  │──1:N──> rental_cars
  │──1:N──> route_segments
  │──1:N──> budget_items
  │──1:N──> weather
```

---

## 1. trips — 旅行计划

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | INT PK AUTO_INCREMENT | ✓ | |
| name | VARCHAR(200) | ✓ | 旅行名称，如"青甘大环线2026" |
| description | TEXT | | 旅行简介 |
| start_date | DATE | | |
| end_date | DATE | | |
| status | ENUM('planning','active','completed') | ✓ | 默认 planning |
| created_at | DATETIME | ✓ | |
| updated_at | DATETIME | ✓ | |

## 2. days — 每日行程

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | INT PK AUTO_INCREMENT | ✓ | |
| trip_id | INT FK→trips.id | ✓ | |
| day_number | INT | ✓ | D0, D1, D2... |
| date | DATE | | |
| title | VARCHAR(200) | | 如"西宁 → 祁连" |
| drive_hours | DECIMAL(3,1) | | 驾驶时长 |
| hotel_city | VARCHAR(100) | | 住宿城市 |
| sort_order | INT | ✓ | 排序 |

## 3. spots — 坐标点

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | INT PK AUTO_INCREMENT | ✓ | |
| trip_id | INT FK→trips.id | ✓ | |
| day_id | INT FK→days.id | | 所属天 |
| name | VARCHAR(200) | ✓ | |
| lng | DECIMAL(10,6) | ✓ | 经度 |
| lat | DECIMAL(10,6) | ✓ | 纬度 |
| category | ENUM('airport','highspeed_rail','train','scenic','photo','hotel','restaurant','other') | ✓ | 坐标类型 |
| is_nav_point | BOOLEAN | | 是否为导航点 |
| nav_order | INT | | 导航顺序 |
| arrival_time | TIME | | 预计到达时间 |
| description | VARCHAR(500) | | 简短描述 |
| intro | TEXT | | 详细介绍 |
| created_at | DATETIME | ✓ | |
| updated_at | DATETIME | ✓ | |

## 4. flights — 航班

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | INT PK AUTO_INCREMENT | ✓ | |
| trip_id | INT FK→trips.id | ✓ | |
| flight_no | VARCHAR(20) | ✓ | 航班号 |
| airline | VARCHAR(100) | | 航空公司 |
| departure_city | VARCHAR(100) | ✓ | |
| departure_airport | VARCHAR(200) | | |
| arrival_city | VARCHAR(100) | ✓ | |
| arrival_airport | VARCHAR(200) | | |
| departure_time | DATETIME | ✓ | |
| arrival_time | DATETIME | ✓ | |
| duration_min | INT | | 飞行时长（分钟） |
| price | DECIMAL(10,2) | | |
| seat_class | VARCHAR(50) | | 经济舱/商务舱/头等舱 |
| booking_link | VARCHAR(500) | | |
| notes | TEXT | | |

## 5. highspeed_rails — 高铁

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | INT PK AUTO_INCREMENT | ✓ | |
| trip_id | INT FK→trips.id | ✓ | |
| train_no | VARCHAR(20) | ✓ | 车次 |
| departure_city | VARCHAR(100) | ✓ | |
| departure_station | VARCHAR(200) | ✓ | |
| arrival_city | VARCHAR(100) | ✓ | |
| arrival_station | VARCHAR(200) | ✓ | |
| departure_time | DATETIME | ✓ | |
| arrival_time | DATETIME | ✓ | |
| duration_min | INT | | |
| price | DECIMAL(10,2) | | |
| seat_class | VARCHAR(50) | | 二等座/一等座/商务座 |
| booking_link | VARCHAR(500) | | |
| notes | TEXT | | |

## 6. rental_cars — 租车

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | INT PK AUTO_INCREMENT | ✓ | |
| trip_id | INT FK→trips.id | ✓ | |
| platform | VARCHAR(100) | | 一嗨/神州 |
| car_name | VARCHAR(200) | ✓ | |
| daily_price | DECIMAL(10,2) | | |
| engine | VARCHAR(100) | | 排量 |
| seats | INT | | |
| trunk | VARCHAR(100) | | 后备箱 |
| notes | TEXT | | |

## 7. route_segments — 导航路段

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | INT PK AUTO_INCREMENT | ✓ | |
| trip_id | INT FK→trips.id | ✓ | |
| from_spot_id | INT FK→spots.id | | |
| to_spot_id | INT FK→spots.id | | |
| distance_km | DECIMAL(8,2) | | |
| duration_min | INT | | |
| polyline | TEXT | | 高德 REST API 返回的 polyline |
| color | VARCHAR(20) | | 路线颜色 |
| day_number | INT | | |

## 8. hotels — 酒店

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | INT PK AUTO_INCREMENT | ✓ | |
| trip_id | INT FK→trips.id | ✓ | |
| spot_id | INT FK→spots.id | | 关联坐标点 |
| city | VARCHAR(100) | ✓ | |
| name | VARCHAR(300) | ✓ | |
| brand | VARCHAR(200) | | 品牌 |
| rating | DECIMAL(2,1) | | 评分 |
| opened_year | INT | | 开业/装修年份 |
| price_per_room | DECIMAL(10,2) | | 每晚价格 |
| room_type | VARCHAR(200) | | 房型 |
| features | JSON | | ["近景区","免费停车","供氧"] |
| check_in_date | DATE | | |
| check_out_date | DATE | | |
| lng | DECIMAL(10,6) | | |
| lat | DECIMAL(10,6) | | |
| phone | VARCHAR(50) | | |
| cover_image | VARCHAR(500) | | 封面图片 URL |
| notes | TEXT | | |

## 9. restaurants — 餐厅

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | INT PK AUTO_INCREMENT | ✓ | |
| trip_id | INT FK→trips.id | ✓ | |
| spot_id | INT FK→spots.id | | 关联坐标点 |
| city | VARCHAR(100) | ✓ | |
| name | VARCHAR(300) | ✓ | |
| address | VARCHAR(500) | | |
| lng | DECIMAL(10,6) | | |
| lat | DECIMAL(10,6) | | |
| rating | DECIMAL(2,1) | | |
| avg_price | DECIMAL(10,2) | | 人均价格 |
| cuisine | VARCHAR(200) | | 菜系 |
| phone | VARCHAR(50) | | |
| opening_hours | VARCHAR(200) | | |
| maps_url | VARCHAR(500) | | 高德导航链接 |
| cover_image | VARCHAR(500) | | |
| notes | TEXT | | |

## 10. dishes — 菜品

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | INT PK AUTO_INCREMENT | ✓ | |
| restaurant_id | INT FK→restaurants.id | ✓ | |
| name | VARCHAR(200) | ✓ | |
| price | DECIMAL(10,2) | | |
| description | TEXT | | |
| image | VARCHAR(500) | | |
| is_signature | BOOLEAN | | 招牌菜 |

## 11. daily_meals — 每日饮食安排

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | INT PK AUTO_INCREMENT | ✓ | |
| day_id | INT FK→days.id | ✓ | |
| restaurant_id | INT FK→restaurants.id | ✓ | |
| meal_type | ENUM('breakfast','lunch','dinner','snack') | ✓ | |
| notes | TEXT | | |

## 12. attractions — 景点详情

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | INT PK AUTO_INCREMENT | ✓ | |
| spot_id | INT FK→spots.id | ✓ | 1:1 关联 |
| ticket_price | VARCHAR(100) | | 如"¥80" |
| opening_hours | VARCHAR(200) | | 如"8:00-18:00" |
| best_season | VARCHAR(200) | | |
| best_time_of_day | VARCHAR(100) | | 如"16:00-日落" |
| duration_hours | DECIMAL(3,1) | | 建议游玩时长 |
| altitude | INT | | 海拔 |
| tips | TEXT | | 游玩建议 |
| highlights | JSON | | ["丹霞+草原+雪峰同框"] |
| must_see | BOOLEAN | | 必看 |

## 13. social_notes — 小红书/抖音笔记

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | INT PK AUTO_INCREMENT | ✓ | |
| spot_id | INT FK→spots.id | ✓ | |
| platform | ENUM('xiaohongshu','douyin') | ✓ | |
| note_id | VARCHAR(100) | ✓ | 小红书 note_id / 抖音 aweme_id |
| title | VARCHAR(500) | | |
| author | VARCHAR(200) | | |
| author_id | VARCHAR(100) | | |
| likes | INT | | |
| comments | INT | | |
| shares | INT | | |
| description | TEXT | | 正文 |
| xsec_token | VARCHAR(200) | | 小红书 xsec_token |
| source_url | VARCHAR(500) | | 原始链接 |
| note_type | VARCHAR(50) | | normal/video |
| fetched_at | DATETIME | | 采集时间 |

## 14. social_images — 笔记图片

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | INT PK AUTO_INCREMENT | ✓ | |
| note_id | INT FK→social_notes.id | ✓ | |
| url | VARCHAR(500) | | 原始 URL |
| url_large | VARCHAR(500) | | 高清 URL |
| width | INT | | |
| height | INT | | |
| sort_order | INT | | 排序 |
| local_path | VARCHAR(500) | | 服务器本地路径 |

## 15. budget_items — 费用明细

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | INT PK AUTO_INCREMENT | ✓ | |
| trip_id | INT FK→trips.id | ✓ | |
| category | ENUM('flight','hotel','car','food','ticket','rail','other') | ✓ | |
| item | VARCHAR(300) | ✓ | |
| unit_price | DECIMAL(10,2) | | |
| quantity | INT | | |
| subtotal | DECIMAL(10,2) | | |
| note | TEXT | | |

## 16. weather — 天气

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | INT PK AUTO_INCREMENT | ✓ | |
| trip_id | INT FK→trips.id | ✓ | |
| city | VARCHAR(100) | ✓ | |
| date | DATE | ✓ | |
| high_temp | VARCHAR(20) | | |
| low_temp | VARCHAR(20) | | |
| weather_desc | VARCHAR(200) | | |
| advice | TEXT | | |

## 17. auth_tokens — 设备认证

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | INT PK AUTO_INCREMENT | ✓ | |
| device_id | VARCHAR(200) | ✓ | 设备唯一标识 |
| token | VARCHAR(500) | ✓ | JWT token |
| expires_at | DATETIME | ✓ | 7 天后过期 |
| created_at | DATETIME | ✓ | |

---

## 索引

```sql
-- trips
CREATE INDEX idx_trips_status ON trips(status);

-- spots
CREATE INDEX idx_spots_trip ON spots(trip_id);
CREATE INDEX idx_spots_day ON spots(day_id);
CREATE INDEX idx_spots_category ON spots(category);
CREATE INDEX idx_spots_nav ON spots(trip_id, is_nav_point, nav_order);

-- social_notes
CREATE INDEX idx_notes_spot ON social_notes(spot_id);
CREATE INDEX idx_notes_platform ON social_notes(platform);

-- 所有 FK 默认建索引
```

## 外键策略

- 全部使用 `ON DELETE CASCADE`：删除 trip 时级联删除所有关联数据
- 删除 spot 时级联删除关联的 attractions / social_notes / hotels / restaurants