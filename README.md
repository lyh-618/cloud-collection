# 云端收藏馆（Cloud Collection）

个人兴趣收藏网站的全栈单仓库。当前阶段聚焦鞠婧祎作品、舞台与入坑路线的安利内容，后续扩展个人收藏、推荐系统和云端部署。

## 当前技术栈

- 前端：Vue 3、TypeScript、Vite
- 后端：Python、FastAPI
- 规划中：MySQL、SQLAlchemy、Alembic、Redis、Docker Compose

## 目录

```text
cloud-collection/
├── frontend/  # Vue 3 + TypeScript + Vite
├── backend/   # FastAPI API
└── docs/      # 学习笔记与项目设计
```

## 本地运行

### 后端

```powershell
cd backend
..\..\AppData\Local\Programs\Python\Python312\python.exe -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### 前端

```powershell
cd frontend
npm install
npm run dev
```

打开 <http://localhost:5173>，页面会通过 Vite 代理请求后端 `/api/health`。

## 学习路线

见 [docs/01-project-initialization.md](docs/01-project-initialization.md)。每一步都说明技术选择、数据流和下一阶段的实践目标。

