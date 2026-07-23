# TRACE.md — 开发日志

## 2026-07-23

- 创建 getaway_plan_v1 项目目录
- 搭建 FastAPI 后端骨架（16 个 router、17 个 model、Pydantic schemas、JWT 认证）
- 搭建 React 前端（14 个组件、响应式布局、高德地图）
- 完成 Docker Compose 配置（db/mysql:8.0 + api/FastAPI + nginx）
- 完成 nginx 配置（API 代理 + 照片 serve + SPA fallback）
- 部署到服务器（`http://27.18.114.8:10338/`）
- 从 qinggan-travel 迁移数据到数据库：
  - 2 trips、7 days、27 spots、10 hotels、10 restaurants、50 dishes
  - 8 budget items、629 social notes、6019 social images
- 从服务器复制 photos 目录（2.6GB / 6671 张图片）
- 复制数据文件（photos.ts、photos_raw.json、weather.ts、rental.ts）
- Git push 超时（不影响代码完整性）
- 当前阻塞：无
