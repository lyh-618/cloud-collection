# 第 1 阶段：项目初始化

## 为什么使用单仓库

前端和后端放在同一个 Git 仓库中，便于一次提交记录一个完整功能，也能共享 README、文档和后续的 Docker Compose 配置。`frontend` 与 `backend` 仍然保持边界清晰，避免互相混入依赖。

## 为什么使用 Vite + Vue 3 + TypeScript

- Vue 3 负责组件化 UI 和响应式状态。
- TypeScript 在编辑阶段检查接口数据和函数参数，减少前后端联调时的低级错误。
- Vite 提供快速开发服务器；开发环境中的 `/api` 代理会把请求转发到 FastAPI，浏览器无需直接处理跨域。

## 为什么先做健康检查

`GET /api/health` 是最小的端到端链路：前端发起 HTTP 请求，Vite 转发请求，FastAPI 返回 JSON，页面再根据响应展示状态。链路成功后，再加入数据库、登录和业务模型，排错范围更小。

## 下一步

1. 将健康检查替换为宠物列表 API。
2. 引入 SQLAlchemy 数据模型和 Alembic 迁移。
3. 使用 MySQL 保存宠物与收藏关系，Redis 缓存热门列表。
4. 增加 Docker Compose，让应用、MySQL 和 Redis 可重复启动。

