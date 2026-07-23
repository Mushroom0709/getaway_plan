# TASKS.md — getaway_plan

## 任务总览

| 阶段 | 名称 | 任务数 | 预估工时 | 依赖 |
|------|------|--------|----------|------|
| P0 | 项目基建 | 5 | 30min | — |
| P1 | 后端基础设施 | 4 | 45min | P0 |
| P2 | 后端核心 API | 4 | 60min | P1 |
| P3 | 后端出行 API | 3 | 30min | P1 |
| P4 | 后端住宿饮食 API | 4 | 45min | P1 |
| P5 | 后端内容 API | 3 | 30min | P1 |
| P6 | 后端杂项 API | 2 | 20min | P1 |
| P7 | 前端基建 | 4 | 45min | P0 |
| P8 | 前端地图 | 3 | 60min | P7 |
| P9 | 前端 UI 组件 | 8 | 120min | P7 |
| P10 | 部署上线 | 4 | 30min | P2-P9 |
| **总计** | | **40** | **~8.5h** | |

---

## P0: 项目基建

### T0-1: 项目目录骨架
- 创建 backend/ 和 frontend/ 目录结构
- 创建 docs/ 目录（已有 5 份设计文档）
- 创建 .gitignore（venv, __pycache__, node_modules, .DS_Store, dist/）
- 验证: `ls -R` 目录结构正确

### T0-2: Docker Compose 配置
- 编写 docker-compose.yml（db + api + nginx）
- 编写 nginx.conf
- 编写 .env.example
- 验证: `docker compose config` 无语法错误

### T0-3: 后端 package 配置
- 创建 backend/requirements.txt
- FastAPI, uvicorn, SQLAlchemy[asyncio], aiomysql, alembic, PyJWT, bcrypt, httpx, pydantic
- 验证: `pip install -r requirements.txt` 成功

### T0-4: 前端 package 配置
- 创建 frontend/package.json（React 19, Vite 8, Tailwind CSS v4, Axios, Phosphor icons）
- 创建 frontend/vite.config.ts
- 创建 frontend/tailwind.config.ts
- 创建 frontend/tsconfig.json
- 验证: `npm install` 成功

### T0-5: Git 初始化
- `git init` + `git remote add origin https://github.com/Mushroom0709/getaway_plan`
- 首次提交（设计文档 + 项目骨架）
- 验证: `git log` 有提交记录

---

## P1: 后端基础设施

### T1-1: FastAPI 骨架 + 配置
- backend/app/main.py：FastAPI 入口，CORS，router 注册
- backend/app/config.py：DATABASE_URL, JWT_SECRET, AMAP_KEY, ACCESS_PASSWORD_HASH
- backend/app/database.py：SQLAlchemy async engine + session
- backend/app/deps.py：get_db 依赖注入
- 验证: `uvicorn app.main:app` 启动，GET /api/health 返回 200

### T1-2: SQLAlchemy 模型（17 张表）
- backend/app/models/ 下全部 17 个 ORM 模型
- 外键 + 级联删除 + 索引
- 验证: `python -c "from app.models import *; print('OK')"` 无报错

### T1-3: Alembic 初始化 + 迁移
- `alembic init` 初始化
- 配置 alembic/env.py（async + 自动发现模型）
- 生成初始迁移 → `alembic upgrade head`
- 验证: MySQL 中 17 张表全部创建

### T1-4: 认证模块
- backend/app/models/auth_token.py
- backend/app/schemas/auth.py
- backend/app/services/auth_service.py：bcrypt 校验 + JWT 生成
- backend/app/routers/auth.py：POST /api/auth/login, GET /api/auth/verify
- 中间件：校验 Bearer token
- 验证: curl 登录获取 token，curl verify 返回 valid

---

## P2: 后端核心 API

### T2-1: Trips CRUD
- POST /api/trips, GET /api/trips, GET /api/trips/{id}, PUT /api/trips/{id}, DELETE /api/trips/{id}
- GET /api/trips/{id} 包含嵌套数据（days, flights, budget_items 等）
- 验证: curl CRUD 全部操作

### T2-2: Days CRUD
- GET /api/trips/{trip_id}/days, POST, PUT /api/days/{id}, DELETE /api/days/{id}
- 验证: curl CRUD

### T2-3: Spots CRUD + 批量排序
- GET /api/trips/{trip_id}/spots（支持筛选 day_id, category, is_nav_point）
- POST /api/trips/{trip_id}/spots, PUT /api/spots/{id}, DELETE /api/spots/{id}
- PUT /api/trips/{trip_id}/spots/reorder（批量更新 nav_order）
- 验证: curl CRUD + reorder

### T2-4: 高德路线规划服务
- backend/app/services/route_service.py：调用高德 REST API
- POST /api/trips/{trip_id}/routes/plan
- GET /api/trips/{trip_id}/routes, DELETE /api/routes/{id}
- 验证: curl plan 返回 distance + polyline

---

## P3: 后端出行 API

### T3-1: Flights CRUD
- GET/POST /api/trips/{trip_id}/flights, PUT/DELETE /api/flights/{id}
- 验证: curl CRUD

### T3-2: Highspeed Rails CRUD
- GET/POST /api/trips/{trip_id}/rails, PUT/DELETE /api/rails/{id}
- 验证: curl CRUD

### T3-3: Rental Cars CRUD
- GET/POST /api/trips/{trip_id}/cars, PUT/DELETE /api/cars/{id}
- 验证: curl CRUD

---

## P4: 后端住宿饮食 API

### T4-1: Hotels CRUD
- GET/POST /api/trips/{trip_id}/hotels, PUT/DELETE /api/hotels/{id}
- 验证: curl CRUD

### T4-2: Restaurants CRUD
- GET/POST /api/trips/{trip_id}/restaurants, PUT/DELETE /api/restaurants/{id}
- 验证: curl CRUD

### T4-3: Dishes CRUD
- GET/POST /api/restaurants/{restaurant_id}/dishes, PUT/DELETE /api/dishes/{id}
- 验证: curl CRUD

### T4-4: Daily Meals CRUD
- GET/POST /api/days/{day_id}/meals, DELETE /api/meals/{id}
- 验证: curl CRUD

---

## P5: 后端内容 API

### T5-1: Attractions CRUD
- GET/POST /api/spots/{spot_id}/attraction, PUT/DELETE /api/attractions/{id}
- 验证: curl CRUD

### T5-2: Social Notes CRUD（含级联创建 images）
- GET/POST /api/spots/{spot_id}/notes, DELETE /api/notes/{id}
- POST 时同时创建 social_images
- 验证: curl 创建 note + images，验证级联

### T5-3: Social Images
- GET /api/notes/{note_id}/images, DELETE /api/images/{id}
- 验证: curl

---

## P6: 后端杂项 API

### T6-1: Budget Items CRUD
- GET/POST /api/trips/{trip_id}/budget, PUT/DELETE /api/budget/{id}
- 验证: curl CRUD

### T6-2: Weather CRUD
- GET/POST /api/trips/{trip_id}/weather, PUT/DELETE /api/weather/{id}
- 验证: curl CRUD

---

## P7: 前端基建

### T7-1: Vite + React 项目初始化
- frontend/src/main.tsx, App.tsx, index.html
- Tailwind CSS v4 配置
- 全局 CSS 变量（taste skill 色板）
- 验证: `npm run dev` 启动，页面显示

### T7-2: API 服务层
- frontend/src/services/api.ts：Axios 实例，JWT 拦截器，401 处理
- API 函数封装（auth, trips, spots, hotels, restaurants...）
- 验证: 调用 /api/auth/login 返回 token

### T7-3: 认证 UI
- frontend/src/components/LoginPage.tsx：密码输入 + 提交
- frontend/src/components/AuthGuard.tsx：token 检查，未登录显示 LoginPage
- frontend/src/hooks/useAuth.ts
- 验证: 页面加载 → 登录页 → 输入密码 → 进入主页

### T7-4: 路由框架
- frontend/src/components/TripSelector.tsx：下拉选择旅行
- frontend/src/hooks/useTrip.ts：加载 trip 数据
- 验证: 选择 trip 后加载数据

---

## P8: 前端地图

### T8-1: 高德地图容器
- frontend/src/hooks/useAmap.ts：动态加载高德 JS SDK
- frontend/src/components/MapPanel.tsx：地图容器
- 验证: 地图显示，支持缩放拖拽

### T8-2: 标记渲染
- frontend/src/components/SpotMarkers.tsx：3 类标记（scenic/photo/hotel）
- 点击标记 → 触发 InfoWindow
- 验证: 标记正确显示，点击弹出信息

### T8-3: 路线渲染
- frontend/src/components/RouteLines.tsx：从 API 获取 route_segments
- AMap.Polyline(showDir: true) 渲染方向箭头
- 按 day_number 切换显示
- 验证: 路线正确显示，箭头方向正确

---

## P9: 前端 UI 组件

### T9-1: 主布局
- frontend/src/components/MainLayout.tsx：响应式两栏/单栏
- PC: grid-cols-[55%_45%]，移动: 40vh + 卡片流
- 验证: 浏览器缩放，布局切换正确

### T9-2: 顶部导航
- frontend/src/components/TopNav.tsx：D0-D6 + 💰费用 按钮
- 横向滚动，移动端紧凑模式
- 验证: 点击切换 day，active 高亮

### T9-3: 当日行程
- frontend/src/components/DayContent.tsx：时间线 + 天气 + 驾驶时长
- 验证: 切换 day 内容更新

### T9-4: 滑出面板
- frontend/src/components/SlidePanel.tsx：右侧滑出动画
- 根据 spot.category 分发子组件
- 验证: 点击标记 → 面板滑出 → 关闭按钮

### T9-5: 酒店详情
- frontend/src/components/HotelDetail.tsx：品牌、评分、价格、房型、特色标签
- 验证: 数据正确渲染

### T9-6: 餐厅详情
- frontend/src/components/RestaurantDetail.tsx：菜品横滑卡片
- 验证: 菜品列表正确显示

### T9-7: 景点详情 + 笔记入口
- frontend/src/components/AttractionDetail.tsx：票价、营业时间、亮点
- 小红书/抖音笔记入口按钮
- 验证: 详情正确渲染

### T9-8: 图片浏览器 + 全屏 Lightbox
- frontend/src/components/PhotoGallery.tsx：按笔记分组，网格展示
- frontend/src/components/Lightbox.tsx：全屏，左右切换，键盘支持
- 验证: 图片加载，点击放大，← → 切换，Esc 关闭

---

## P10: 部署上线

### T10-1: Dockerfile
- backend/Dockerfile：python:3.12-slim，pip install，uvicorn
- 验证: `docker build -t getaway-api .` 成功

### T10-2: 前端构建配置
- vite.config.ts：prod build，proxy 配置
- 验证: `npm run build` 成功，dist/ 产出

### T10-3: docker-compose 编排
- 整合 db + api + nginx
- 环境变量注入
- 验证: `docker compose up -d`，curl 访问

### T10-4: 服务器部署
- SSH 到 ecs-xj-ai-service (27.18.114.8:10332)
- scp 项目文件 → docker compose up -d
- 端口 10338，路由 /travel/
- 验证: curl http://27.18.114.8:10338/api/health 返回 200

---

## 并行执行建议

```
P0 (基建)
 ├── P1 (后端基础设施)
 │    ├── P2 (核心 API) ──┐
 │    ├── P3 (出行 API)   ├── P10 (部署)
 │    ├── P4 (住宿饮食)    │
 │    ├── P5 (内容 API)    │
 │    └── P6 (杂项 API) ──┘
 └── P7 (前端基建)
      ├── P8 (前端地图) ──┐
      └── P9 (前端 UI) ───┘
```

- P0 完成后，P1 和 P7 可并行
- P1 完成后，P2-P6 可并行（不同路由文件，无冲突）
- P7 完成后，P8 和 P9 可并行
- P2-P9 全部完成后，执行 P10