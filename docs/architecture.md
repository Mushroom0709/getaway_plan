# Architecture Design — getaway_plan

## 1. 总体架构

```
┌──────────────────────────────────────────────────────────────────┐
│                          浏览器                                   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │               React 19 SPA (Vite + Tailwind CSS v4)      │   │
│  │  ┌──────────────────────────────────────────────────┐   │   │
│  │  │              全屏高德地图 (AMap JS API 2.0)       │   │   │
│  │  │   · 47 个标记 (scenic/photo/hotel/rest...)  │   │   │
│  │  │   · 22 条自驾路线 (实线+箭头)                    │   │   │
│  │  │   · 3 条 transit 路线 (虚线, 航班)                     │   │   │
│  │  └──────────────────────────────────────────────────┘   │   │
│  │  ┌──────────────────────────────────────────────────┐   │   │
│  │  │  悬浮顶栏 (TripSelector + DayNav Tabs)           │   │   │
│  │  └──────────────────────────────────────────────────┘   │   │
│  │  ┌──────────────────────────────────────────────────┐   │   │
│  │  │  右侧滑出面板 (酒店/景点/笔记/美食/城市详情)      │   │   │
│  │  └──────────────────────────────────────────────────┘   │   │
│  └──────────────────────────────────────────────────────────┘   │
│  Axios ←── JWT Token (7天) ──→ /api/*                           │
└──────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────────┐
│                  Nginx (alpine, 端口 ${NGINX_PORT})                       │
│  /          → dist/index.html (SPA)                              │
│  /api/*     → proxy_pass http://api:8000/api/                    │
│  /photos/*  → serve 静态照片目录                                  │
└──────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────────┐
│              FastAPI (python:3.12-slim, 端口 8000)                │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐       │
│  │  auth    │  │  trips   │  │  spots   │  │  hotels  │       │
│  │  router  │  │  router  │  │  router  │  │  router  │       │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘       │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐       │
│  │restaurant│  │ flights  │  │  rails   │  │  budget  │       │
│  │  router  │  │  router  │  │  router  │  │  router  │       │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘       │
│  ┌──────────┐  ┌──────────────────────────────────┐           │
│  │  routes  │  │  route_service                    │           │
│  │  router  │  │  (高德规划 driving + 直接创建 transit)│        │
│  └──────────┘  └──────────────────────────────────┘           │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐                    │
│  │  notes   │  │  weather │  │  meals   │                    │
│  │  router  │  │  router  │  │  router  │                    │
│  └──────────┘  └──────────┘  └──────────┘                    │
│  SQLAlchemy 2.0 (async) + Alembic (2 migrations)              │
└──────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────────┐
│              MySQL 8.0 (端口 3306, 内网)                          │
│  Database: getaway_plan                                         │
│  17 张表                                                         │
└──────────────────────────────────────────────────────────────────┘
```

## 2. 技术栈

| 层 | 选型 | 版本 | 说明 |
|----|------|------|------|
| 框架 | FastAPI | 0.115+ | 异步，自带 OpenAPI |
| ORM | SQLAlchemy | 2.0 | async session |
| 迁移 | Alembic | latest | |
| 数据库 | MySQL | 8.0 | Docker 容器 |
| 认证 | PyJWT | latest | 7 天过期 |
| 密码 | bcrypt | latest | 单密码哈希存储 |
| 前端 | React | 19 | SPA |
| 构建 | Vite | 8 | |
| 样式 | Tailwind CSS | v4 | taste skill 视觉体系 |
| 图标 | @phosphor-icons/react | latest | |
| 地图 | 高德 JS API | 2.0 | key 通过 VITE_AMAP_KEY 环境变量配置 |
| 路线 | 高德 REST API | v3 | /v3/direction/driving |
| HTTP | Axios | latest | 前端请求 |
| 部署 | Docker Compose | — | 2 容器 |
| Web 服务器 | Nginx | alpine | serve 前端 + proxy API |

## 3. 项目目录结构

```
getaway_plan_v1/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI 入口
│   │   ├── config.py            # 配置 (DB, JWT secret, 密码 hash)
│   │   ├── database.py          # SQLAlchemy engine + session
│   │   ├── models/              # ORM 模型
│   │   │   ├── trip.py
│   │   │   ├── day.py
│   │   │   ├── spot.py
│   │   │   ├── flight.py
│   │   │   ├── highspeed_rail.py
│   │   │   ├── rental_car.py
│   │   │   ├── route_segment.py
│   │   │   ├── hotel.py
│   │   │   ├── restaurant.py
│   │   │   ├── dish.py
│   │   │   ├── daily_meal.py
│   │   │   ├── attraction.py
│   │   │   ├── social_note.py
│   │   │   ├── social_image.py
│   │   │   ├── budget_item.py
│   │   │   ├── weather.py
│   │   │   └── auth_token.py
│   │   ├── schemas/             # Pydantic schemas
│   │   ├── routers/             # API 路由
│   │   │   ├── auth.py
│   │   │   ├── trips.py
│   │   │   ├── spots.py
│   │   │   ├── flights.py
│   │   │   ├── highspeed_rails.py
│   │   │   ├── rental_cars.py
│   │   │   ├── route_segments.py
│   │   │   ├── hotels.py
│   │   │   ├── restaurants.py
│   │   │   ├── dishes.py
│   │   │   ├── daily_meals.py
│   │   │   ├── attractions.py
│   │   │   ├── social_notes.py
│   │   │   ├── social_images.py
│   │   │   ├── budget_items.py
│   │   │   └── weather.py
│   │   ├── services/            # 业务逻辑
│   │   │   ├── auth_service.py
│   │   │   └── route_service.py  # 高德 REST API 调用
│   │   └── deps.py              # 依赖注入
│   ├── alembic/
│   ├── requirements.txt
│   ├── Dockerfile
│   └── tests/
├── frontend/
│   ├── src/
│   │   ├── components/          # React 组件
│   │   ├── hooks/               # useAmap, useAuth, useTrip...
│   │   ├── services/            # Axios API 封装
│   │   ├── types.ts
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── public/
│   ├── package.json
│   ├── vite.config.ts
│   └── tailwind.config.ts
├── docker-compose.yml
├── nginx.conf
├── docs/
│   ├── architecture.md          # 本文件
│   ├── database-schema.md
│   ├── api-specs.md
│   ├── module-specs.md
│   └── AI_AGENT_API.md
├── AGENTS.md
├── DIR.md
├── PRD.md
├── TASKS.md
└── TRACE.md
```

## 4. 认证流程

```
1. 用户打开页面 → 检测 localStorage 无 token → 显示登录页
2. 用户输入密码 → POST /api/auth/login { password }
3. 后端 bcrypt 校验 → 生成 JWT (7天过期) → 存 auth_tokens 表
4. 前端存 token 到 localStorage → Axios 拦截器注入 Authorization: Bearer xxx
5. 后续请求自动带 token → 后端中间件校验
6. 401 → 前端清除 token → 跳转登录页
```

**密码管理**：密码哈希存储在环境变量 `ACCESS_PASSWORD_HASH` 中，不存数据库。

## 5. 高德地图集成

### 前端 (JS API 2.0)
- 加载：`<script src="https://webapi.amap.com/maps?v=2.0&key=KEY">`
- 标记：AMap.Marker（自定义 HTML content）
- 路线：AMap.Polyline（showDir: true 显示方向箭头）
- 信息窗：AMap.InfoWindow（isCustom: true）
- 定位：AMap.Geolocation

### 后端 (REST API)
- 路线规划：`GET /api/route/plan?origin=lng,lat&dest=lng,lat`
- 调用高德 `restapi.amap.com/v3/direction/driving`
- 返回 polyline 存入 route_segments 表
- 前端从 API 获取 route_segments 后渲染 Polyline

## 6. 部署

### docker-compose.yml
```yaml
services:
  db:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: ${MYSQL_ROOT_PASSWORD}
      MYSQL_DATABASE: getaway_plan
    volumes:
      - mysql_data:/var/lib/mysql
    ports:
      - "3306:3306"
    restart: always

  api:
    build: ./backend
    depends_on:
      - db
    environment:
      DATABASE_URL: mysql+aiomysql://root:${MYSQL_ROOT_PASSWORD}@db:3306/getaway_plan
      JWT_SECRET: ${JWT_SECRET}
      ACCESS_PASSWORD_HASH: ${ACCESS_PASSWORD_HASH}
      AMAP_KEY: ${AMAP_KEY}
    volumes:
      - ./frontend/dist:/app/static
    restart: always

  nginx:
    image: nginx:alpine
    ports:
      - "10338:80"
    volumes:
      - ./nginx.conf:/etc/nginx/conf.d/default.conf
      - ./frontend/dist:/usr/share/nginx/html
    depends_on:
      - api
    restart: always

volumes:
  mysql_data:
```

### Nginx 配置
```nginx
server {
    listen 80;
    server_name _;

    location /api/ {
        proxy_pass http://api:8000/api/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /photos/ {
        alias /opt/photos/;
    }

    location / {
        root /usr/share/nginx/html;
        try_files $uri $uri/ /index.html;
    }
}
```

## 7. 架构决策记录 (ADR)

### ADR-0001: 前后端分离，前端只读展示
- 决策：AI Agent 通过 API 操作数据，前端仅展示
- 原因：用户明确要求

### ADR-0002: JWT 7 天过期
- 决策：单密码 + JWT + 7 天过期
- 原因：单用户模式，无需复杂认证

### ADR-0003: 飞机和高铁分表
- 决策：flights 和 highspeed_rails 独立两张表
- 原因：字段差异大（高铁有 station，飞机有 airport/airline）

### ADR-0004: 高德路线用 REST API
- 决策：后端调用高德 REST API，前端渲染 Polyline
- 原因：Web 服务 Key 不支持 JS Driving 插件，REST API 已验证可用

### ADR-0005: Docker Compose 两容器
- 决策：api + db，Nginx 整合进 api 容器
- 原因：简化部署，减少容器数量

### ADR-0006: ON DELETE CASCADE
- 决策：所有外键使用级联删除
- 原因：删除 trip 时自动清理全部关联数据，符合单用户场景