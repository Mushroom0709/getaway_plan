# TASKS.md — getaway_plan

## 任务总览

| 阶段 | 名称 | 任务数 | 状态 | 依赖 |
|------|------|--------|------|------|
| P0 | 项目基建 | 5 | ✅ DONE | — |
| P1 | 后端基础设施 | 4 | ✅ DONE | P0 |
| P2 | 后端核心 API | 4 | ✅ DONE | P1 |
| P3 | 后端出行 API | 3 | ✅ DONE | P1 |
| P4 | 后端住宿饮食 API | 4 | ✅ DONE | P1 |
| P5 | 后端内容 API | 3 | ✅ DONE | P1 |
| P6 | 后端杂项 API | 2 | ✅ DONE | P1 |
| P7 | 前端基建 | 4 | ✅ DONE | P0 |
| P8 | 前端地图 | 3 | ✅ DONE | P7 |
| P9 | 前端 UI 组件 | 8 | ✅ DONE | P7 |
| P10 | 部署上线 | 4 | ✅ DONE | P2-P9 |
| P11 | 独立部署重构 | 4 | ✅ DONE | P10 |
| P12 | 数据迁移 | 6 | ✅ DONE | P11 |
| P13 | 前端重构（地图全屏） | 4 | ✅ DONE | P12 |
| P14 | 公共交通路线 | 4 | ✅ DONE | P13 |
| **总计** | | **58** | **✅ 全部完成** | |

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
- SSH 到服务器 (HOST:PORT)
- scp 项目文件 → docker compose up -d
- 端口 ${NGINX_PORT}，路由 /
- 验证: curl http://HOST:PORT/api/health 返回 200

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

---

## P11: 独立部署重构

### T11-1: 项目独立化
- 部署目录: `/home/workspace/mushroom/getaway_plan/`
- MySQL 独立卷: `getaway_plan_v1_mysql_data`
- 停用旧 `/opt/getaway_plan/` 的 docker-compose
- 验证: 三容器独立运行

### T11-2: Alembic 迁移系统搭建
- 创建 `alembic.ini` + `alembic/env.py`（async MySQL）
- 编写 `001_create_all_tables.py`（17 张表初始迁移）
- 验证: `alembic upgrade head` 创建全部表

### T11-3: 密码与配置
- 密码变更为 `2026`，更新 bcrypt hash
- 修复 `auth_token.py` 的 Base 引用（从 trip.py 导入）
- 修复前端 `useTrip.ts` API 路径（budget→budget_items, weather→weathers）
- 验证: curl 登录返回 token

### T11-4: Docker 构建流程
- Dockerfile 恢复为纯 CMD（不含 alembic auto-migrate）
- 迁移手动执行: `docker exec getaway_plan-api-1 sh -c 'cd /app && PYTHONPATH=/app alembic upgrade head'`
- 验证: 迁移成功后 API 返回空数组（空数据库）

---

## P12: 数据迁移

### T12-1: 数据提取
- 使用 tsx 从 qinggan-travel 提取 TS 数据为 JSON
- 输出: itinerary.json, spots.json, hotels.json, food.json, budget.json, weather.json, rental.json, photos.json
- 验证: 8 个 JSON 文件，总计 ~850KB

### T12-2: 导入脚本
- 编写 `scripts/import_data.py`，通过 REST API 调用后端接口导入
- 按顺序创建: Trip → Days → Spots → Attractions → Hotels → Restaurants → Dishes → Budget → Weather → Cars → Social Notes
- 验证: 全部数据入库

### T12-3: 社交笔记导入
- 629 条 social_notes + 6019 张 social_images
- 图片路径映射到服务器 `/opt/getaway_plan/photos/{spot}/{platform}/{author}/`
- nginx `/photos/` 别名已就位
- 验证: Click spot → SlidePanel → PhotoGallery

### T12-4: 路线生成
- 调用高德 API 生成 21 条自驾 route_segments
- 含 day_number、color、polyline
- 4 条超长距离路线失败（张掖→敦煌等跨越不同日期的路段）
- 验证: MapPanel 显示彩色路线

### T12-5: Days 关联
- Spots 的 day_id 关联到正确的 Days
- 26 个原始 spots + 20 个酒店/餐厅 spots 全部关联
- 验证: 切换 DayTab 过滤正确

### T12-6: 更新照片软链接
- `/opt/photos/` → `/opt/getaway_plan/photos/` 软链接
- 验证: `http://HOST:PORT/photos/` 可访问

---

## P13: 前端重构（地图全屏）

### T13-1: MapPanel 全量渲染
- 始终显示全部 46 个 spots（不按 day 过滤）
- 始终显示全部 route_segments
- activeDay 控制高亮/变暗，非过滤
- 修复首次加载不显示：增加 `mapReady` 状态绑定 effect 依赖
- 验证: 选择 trip 后所有标记立即显示

### T13-2: App.tsx 地图优先布局
- 地图占满全屏（h-screen, flex-1）
- 顶栏悬浮半透明（absolute, bg-white/90, backdrop-blur-sm）
- 移除右侧 DayContent 面板
- TripSelector 在所有状态下可见
- 验证: 页面加载即见全屏地图

### T13-3: TopNav "全部" 标签
- 新增 🗺️ 全部 标签，默认选中
- activeDay='all' 时全部标记和路线均等显示
- 验证: 点击各标签切换

### T13-4: SlidePanel 分类详情
- hotel: HotelDetail + 当天行程摘要
- restaurant: RestaurantDetail + dishes + 当天行程
- scenic/photo: AttractionDetail + PhotoGallery + notes
- stay/other: 当天摘要 + 该城市酒店列表
- 验证: 点击各类标记弹出对应详情

---

## P14: 公共交通路线

### T14-1: route_type 字段
- 模型 `route_segment.py` 新增 `route_type`（driving/transit）
- Schema 新增 `RouteCreateRequest`
- 迁移 `002_add_route_type.py`
- 验证: 列创建成功

### T14-2: 直接创建路线 API
- 新增 `POST /api/trips/{id}/routes`（不调用高德 API）
- plan 端点也支持 route_type 字段
- 验证: 可直接创建带 polyline 的路线

### T14-3: 航班虚线路线
- 创建 武汉（airport spot, lng=114.30, lat=30.60）
- 武汉→西宁: transit route（粉色虚线, D0）
- 敦煌→酒泉: transit route（粉色虚线, D6）
- 验证: 地图显示虚线

### T14-4: MapPanel 虚线渲染
- transit 路线: strokeStyle='dashed', strokeDasharray=[10,8], showDir=false
- driving 路线: strokeStyle='solid', showDir=true
- 验证: D0 武汉→西宁 为虚线