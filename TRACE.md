# TRACE.md — 开发日志

## 2026-07-23

### 上午 — 项目搭建与后端开发
- 创建 getaway_plan_v1 项目目录
- 搭建 FastAPI 后端骨架（16 个 router、17 个 model、Pydantic schemas、JWT 认证）
- 搭建 React 前端（14 个组件、响应式布局、高德地图）
- 完成 Docker Compose 配置（db/mysql:8.0 + api/FastAPI + nginx）
- 完成 nginx 配置（API 代理 + 照片 serve + SPA fallback）
- 部署到服务器（通过 Nginx 反向代理）
- 从 qinggan-travel 迁移数据到数据库（旧部署）
- 从服务器复制 photos 目录（2.6GB / 6671 张图片）

### 下午 — 独立部署与问题修复
- **独立部署重构**：项目独立部署到 `/home/workspace/mushroom/getaway_plan/`，MySQL 使用独立卷 `getaway_plan_v1_mysql_data`
- **Alembic 迁移系统**：创建 `alembic.ini`、`env.py`（async）、初始迁移 `001_create_all_tables.py`（17 张表）
- **密码变更**：登录密码设为 `2026`
- **修复模型 Base 引用**：`auth_token.py` 的 Base 改为从 `trip.py` 导入
- **API 路径修复**：前端 `useTrip.ts` 的 budget→budget_items, weather→weathers
- **数据导入**：编写 `scripts/import_data.py`，从 qinggan-travel 的 TS 文件提取数据，通过 REST API 全量导入：
  - 1 trip / 7 days / 46 spots / 10 hotels / 10 restaurants / 50 dishes
  - 21 attractions / 9 budget items / 4 weather / 3 rental cars
  - 629 social notes / 6019 social images
  - 21 条高德自驾路线段
- **前端重构**：地图全屏化
  - MapPanel 改为全量渲染全部标记和路线
  - App.tsx 地图占满全屏，顶栏悬浮半透明
  - TopNav 新增"🗺️ 全部"标签页
  - SlidePanel 按 spot.category 分发不同详情内容
  - hotel→HotelDetail+当天行程, restaurant→RestaurantDetail, scenic→AttractionDetail+Notes, stay→当天摘要+酒店列表
- **修复首次加载不显示**：MapPanel 增加 `mapReady` 状态，确保地图就绪后自动渲染标记
- **公共交通虚线**：新增 `route_type` 字段（driving/transit），添加直接创建路线 API，武汉→西宁、敦煌→酒泉虚线显示

### 服务状态
- 部署地址: 通过环境变量 NGINX_PORT 配置
- 登录密码: 通过环境变量 ACCESS_PASSWORD_HASH 配置（bcrypt hash）
- 工作目录: `/home/workspace/mushroom/getaway_plan/`
- 容器: getaway_plan-db-1, getaway_plan-api-1, getaway_plan-nginx-1
- MySQL: `getaway_plan_v1_mysql_data` 独立卷
- 照片: `/opt/getaway_plan/photos/`（nginx `/photos/` 别名）

## 2026-07-24

### 问题修复
- **修复无限刷新循环**：App.tsx 在未登录时调用 `/api/trips` 触发 401 → axios 拦截器重定向 → 死循环。修复：API 调用前检查 token，AuthGuard 增加 onLogin 回调
- **修复 D6/D7 地图不聚焦**：`day_id`（DB主键）与 `day_number`（D6=6）不匹配（因删除重建导致ID跳跃）。修复：通过 days 数组建立 day_number↔day_id 映射
- **修复 fitView 只看点不看线**：bounds 计算纳入 route polyline 坐标点
- **修复 D7 路线**：删除直线路线(id=53)，保留真实高德自驾路线(id=58, 397km)。新增 transit 路线 酒泉→武汉 和航班 MU2478

### 敏感信息清理
- 所有 IP/端口/密码/API Key 从代码中移除，改用环境变量
- docker-compose.yml 全部使用 ${VAR} 引用
- .env.example 使用占位符
- 脚本改为从环境变量读取配置

### v1.0 发布
- 标记 v1.0 版本
- 当前阻塞：无
