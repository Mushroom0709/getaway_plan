# DIR.md — getaway_plan 目录约束

## 顶层目录

```
getaway_plan_v1/
├── backend/           # FastAPI 后端
├── frontend/          # React + Vite 前端
├── docs/              # 设计文档及 Agent 配置
├── scripts/           # 数据迁移脚本（photos.ts, rental.ts, weather.ts）
├── tasks/             # 任务描述文件（Crush 任务）
├── .crush/            # Crush 引擎数据（自动生成）
└── (项目文档: AGENTS.md, PRD.md, TASKS.md, TRACE.md, DIR.md)
```

## 目录规则

| 目录 | 用途 | 允许新建子目录 | 备注 |
|------|------|---------------|------|
| `backend/` | FastAPI 应用代码 | 否（已有 app/ 和 tests/） | app/ 下已有 models/ routers/ schemas/ services/ |
| `frontend/` | React 前端 | 否（已有 src/components/ hooks/ services/） | 构建产物在 dist/ |
| `docs/` | 设计文档 | 是（按主题） | docs/agents/ 已存在（issue-tracker 等） |
| `scripts/` | 数据迁移脚本 | 否 | TS 和 JSON 原始数据 |
| `tasks/` | 任务描述 | 是（按 phase） | 已有 phase-01 到 phase-10 |
| `.crush/` | Crush 引擎数据 | 否 | 自动生成，不手动修改 |

## 命名规范

- **后端文件**：蛇形命名，如 `attraction.py`, `social_image.py`
- **前端组件**：PascalCase，如 `MapPanel.tsx`, `PhotoGallery.tsx`
- **API 路由**：RESTful 风格，如 `/api/trips/{id}/spots`
- **数据库表**：复数 snake_case，如 `trips`, `budget_items`
- **数据文件**：蛇形命名，如 `photos_raw.json`

## 禁止

- 在项目根目录创建新的顶层目录（必须经用户确认）
- 将代码文件放在项目根目录
- 手动修改 `.crush/` 目录下的文件
- 在 `frontend/dist/` 下手动编辑构建产物
