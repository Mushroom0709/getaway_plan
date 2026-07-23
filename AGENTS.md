# getaway_plan — Agent Context

> FastAPI + React 旅行规划系统。前端 SPA + REST API 后端 + MySQL，数据可持久化编辑。

## 目录结构

```
getaway_plan_v1/
├── backend/                    # FastAPI 后端
│   ├── app/
│   │   ├── main.py            # FastAPI 入口，CORS，17 个 router 注册
│   │   ├── config.py          # Pydantic Settings（DATABASE_URL, JWT_SECRET, AMAP_KEY...）
│   │   ├── database.py        # SQLAlchemy async engine + session
│   │   ├── deps.py            # get_db 依赖注入
│   │   ├── models/            # 17 个 ORM 模型
│   │   ├── routers/           # 16 个业务路由模块
│   │   ├── schemas/           # Pydantic 请求/响应模型
│   │   ├── services/          # auth_service, route_service
│   │   └── __init__.py
│   ├── tests/
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/                   # React + Vite + Tailwind CSS v4
│   ├── src/
│   │   ├── components/        # 14 个组件
│   │   ├── hooks/             # 3 个 hook（useAuth, useIsMobile, useTrip）
│   │   ├── services/api.ts   # Axios + JWT 拦截器
│   │   ├── types.ts           # TypeScript 类型定义
│   │   ├── App.tsx            # 根组件
│   │   └── main.tsx           # 入口
│   ├── dist/                  # 构建产物（已部署）
│   ├── package.json
│   └── vite.config.ts
├── docs/                       # 设计文档
│   ├── agents/                 # Agent 配置（issue-tracker, triage-labels, domain）
│   ├── architecture.md
│   ├── api-specs.md
│   ├── database-schema.md
│   ├── AI_AGENT_API.md
│   └── module-specs.md
├── scripts/                    # 数据迁移脚本
│   ├── photos.ts              # 3127 条照片路径 + 元数据
│   ├── photos_raw.json        # 6786 条原始照片数据
│   ├── weather.ts             # 天气数据
│   └── rental.ts              # 租车数据
├── tasks/                      # Crush 任务描述
├── docker-compose.yml          # db(MySQL:8.0) + api(FastAPI) + nginx(静态文件代理)
├── nginx.conf                  # /api/ → FastAPI, /photos/ → 本地文件, / → SPA
└── .env.example               # MYSQL_PASSWORD / JWT_SECRET / ACCESS_PASSWORD_HASH / AMAP_KEY / NGINX_PORT
```

## 技术栈

| 层 | 选型 | 备注 |
|----|------|------|
| 后端框架 | FastAPI 0.139 + Python 3.12 | async, SQLAlchemy 2.0 |
| 数据库 | MySQL 8.0 | Docker 容器 |
| ORM | SQLAlchemy 2.0 asyncio | 异步引擎，session 依赖注入 |
| 迁移 | Alembic | 自动发现模型 |
| 认证 | bcrypt + PyJWT | POST /api/auth/login → Bearer token |
| 前端框架 | React 19 + TypeScript | Vite 6 构建 |
| 样式 | Tailwind CSS v4 | @tailwindcss/vite 插件 |
| 地图 | 高德 JS API 2.0 | 底图 + 标记 + 路线 polyline |
| 图标 | @phosphor-icons/react | — |
| HTTP | Axios | JWT 拦截器 + 401 跳登录 |
| 部署 | Docker Compose | nginx:alpine + python:3.12-slim |
| 图片 | nginx 直接 serve | /photos/ 别名到服务器本地目录 |
| 镜像源 | pip: mirrors.aliyun.com（Dockerfile 已配置） | npm: registry.npmmirror.com |

## 通信协议

| 服务 | 端口 | 协议 | 说明 |
|------|------|------|------|
| nginx | 10338 | HTTP | 前端 SPA + 静态文件代理 |
| FastAPI | 8000（容器内） | HTTP | REST API，仅 nginx 可访问 |
| MySQL | 3306（容器内） | TCP | 仅 api 容器可访问 |

API 路由前缀：`/api/`
认证：所有 API 除 `/api/auth/login`、`/api/health` 外需 Bearer token

## 数据库模型

17 张表（已迁移数据：7 days / 27 spots / 10 hotels / 10 restaurants / 50 dishes / 8 budget items / 629 social notes / 6019 social images / 2 trips）：

| 表名 | 用途 | 关联 |
|------|------|------|
| trips | 旅行项目 | — |
| days | 日程天 | → trips |
| spots | 地点/景点/标记点 | → trips, days |
| hotels | 酒店 | → spots |
| restaurants | 餐厅 | → spots |
| dishes | 菜品 | → restaurants |
| daily_meals | 每日餐食 | → days |
| attractions | 景点详情 | → spots |
| flights | 航班 | → trips |
| highspeed_rails | 高铁 | → trips |
| rental_cars | 租车 | → trips |
| route_segments | 路线段 | → trips |
| budget_items | 预算项目 | → trips |
| weather | 天气 | → trips |
| social_notes | 小红书/抖音笔记 | → spots |
| social_images | 笔记图片 | → social_notes |
| auth_tokens | JWT 令牌 | — |

## 约束

- 国内镜像源：pip 使用 `mirrors.aliyun.com`，npm 使用 `npmmirror.com`，已在 Dockerfile 和 .npmrc 中配置
- 照片不进 JS 包：JS 只存路径字符串，图片由 nginx 通过 `/photos/` 别名 serve
- 照片路径规则：`/photos/{景点中文}/{小红书|抖音}/{作者}/{5位hash}_{标题}.{ext}`
- 不修改系统级 pip/npm 配置，只在项目级配置
- 可用的前端密码：`admin123`（对应的 bcrypt hash 在 docker-compose.yml 中）
- 高德 API Key: `f2a8c18781eefe2b345d24ca91418e96`

## 已部署服务

- 地址：`http://27.18.114.8:10338/`
- 照片（服务器本地）：`/opt/getaway_plan/photos/`（2.6GB / 6671 张图片）
- 容器：travel-web（nginx:alpine，端口映射 10338:80）
- API 密码：`admin123`

## 术语

| 术语 | 说明 |
|------|------|
| Trip | 一次旅行项目，如"青甘大环线2026" |
| Day | 行程中的一天（D0-D6） |
| Spot | 地图上一个标记点（住宿城市/景区/拍照点） |
| Nav Point | 路线规划途经点（is_nav_point=true） |
| Social Note | 小红书/抖音的笔记内容 |
| Route Segment | 高德 REST API 返回的一段真实道路路线 |
| Budget Item | 一条费用明细（类别/项目/单价/数量/小计） |
