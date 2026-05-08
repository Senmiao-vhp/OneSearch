# OneSearch 一搜

开发者一站式信息搜索工具

## 项目简介

整合CSDN技术博客、知网学术论文、GitHub/Gitee代码仓库四大数据源，提供一站式搜索体验。

## 技术栈

### 前端
- **框架**: Next.js 14
- **语言**: TypeScript
- **样式**: TailwindCSS
- **状态管理**: Zustand
- **数据请求**: Axios + React Query

### 后端
- **框架**: FastAPI
- **语言**: Python 3.11+
- **数据库**: PostgreSQL
- **认证**: JWT + HTTP Only Cookie

## 快速开始

### 前端

```bash
cd frontend
npm install
npm run dev
```

访问 http://localhost:3000

### 后端

```bash
cd backend
python -m venv venv
# Windows: venv\Scripts\activate
# Linux/Mac: source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

访问 http://localhost:8000/docs 查看API文档

## 环境变量

### 后端 (.env)

```env
DATABASE_URL=postgresql://user:password@localhost:5432/onesearch
JWT_SECRET_KEY=your-secret-key
CORS_ORIGINS=http://localhost:3000
# 可选：提升 GitHub API 限额
GITHUB_API_TOKEN=
# 可选：Gitee 搜索仓库（OpenAPI v5），建议配置私人令牌以提高可用性
GITEE_ACCESS_TOKEN=
```

### 前端 (.env.local)

```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
```

## API接口

### 认证模块

| 方法 | 路径 | 描述 |
|------|------|------|
| POST | /api/v1/auth/register | 用户注册 |
| POST | /api/v1/auth/login | 用户登录 |
| POST | /api/v1/auth/logout | 用户登出 |
| GET | /api/v1/auth/me | 获取当前用户 |

### 搜索模块

| 方法 | 路径 | 描述 |
|------|------|------|
| GET | /api/v1/search/repos | GitHub+Gitee 仓库合并搜索（一次请求、按 Star 合并排序） |
| GET | /api/v1/search/github | 仅 GitHub 仓库搜索 |

合并策略：GitHub、Gitee **各自**请求至多 `per_page` 条；合并时按**源内** Star 排序后各占约一半席位并**交错展示**，避免仅以全局 Star 排序时高星 GitHub 占满全页。未配置 `GITEE_ACCESS_TOKEN` 或单侧无结果时，由另一侧顺延补足。

## 项目结构

```
OneSearch/
├── backend/
│   └── app/
│       ├── core/          # 核心配置
│       ├── modules/       # 功能模块
│       │   ├── auth/     # 认证模块
│       │   └── search/   # 搜索模块
│       └── shared/       # 共享模块
│
└── frontend/
    └── src/
        ├── app/          # 页面
        ├── components/   # 组件
        ├── modules/      # 功能模块
        └── lib/          # 工具库
```

## License

MIT
