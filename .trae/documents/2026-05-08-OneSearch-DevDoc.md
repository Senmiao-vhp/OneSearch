# OneSearch 一搜 - 开发文档

**版本：** v1.0  
**日期：** 2026-05-08  
**状态：** 开发中

---

## 1. 项目概述

### 1.1 项目定位
开发者一站式信息搜索工具

### 1.2 核心价值
整合CSDN技术博客、知网学术论文、GitHub/Gitee代码仓库四大数据源，提供一站式搜索体验。

### 1.3 MVP目标
- 用户系统（注册、登录、用户面板）
- GitHub代码仓库搜索
- 验证核心架构可行性

---

## 2. 技术架构

### 2.1 技术栈

| 模块 | 技术选型 | 部署平台 | 说明 |
|------|----------|----------|------|
| 前端 | Next.js | Vercel | SSR支持，SEO友好 |
| 后端 | Python + FastAPI | Railway/云服务器 | 高性能API框架 |
| 数据库 | PostgreSQL | Railway | 关系型数据库 |
| 认证 | HTTP Only Cookie + JWT | - | 安全无状态认证 |

---

## 3. 模块架构

### 3.1 模块划分原则
- **高内聚低耦合**：每个模块职责单一，模块间通过接口通信
- **独立可测试**：每个模块可独立开发、测试
- **并行开发**：模块间无依赖，可同时开发

### 3.2 后端模块划分

```
backend/
├── app/
│   ├── core/                 # 核心基础模块
│   │   ├── config.py         # 配置管理
│   │   ├── database.py       # 数据库连接
│   │   ├── security.py       # 安全工具（JWT、密码加密）
│   │   └── exceptions.py     # 自定义异常
│   │
│   ├── modules/auth/         # 认证模块
│   │   ├── api/              # API路由
│   │   │   └── endpoints.py  # 认证接口声明
│   │   ├── schemas/          # Pydantic模型
│   │   │   ├── request.py    # 请求模型
│   │   │   └── response.py   # 响应模型
│   │   ├── services/         # 服务层（业务逻辑）
│   │   └── repository/       # 数据访问层
│   │
│   ├── modules/search/       # 搜索模块
│   │   ├── api/
│   │   │   └── endpoints.py  # 搜索接口声明
│   │   ├── schemas/
│   │   ├── services/         # 搜索服务
│   │   └── integrations/     # 第三方集成（GitHub API等）
│   │
│   ├── shared/               # 共享模块
│   │   ├── models/          # ORM模型
│   │   └── dependencies.py   # 依赖注入
│   │
│   └── main.py              # 应用入口
```

### 3.3 前端模块划分

```
frontend/
├── src/
│   ├── components/           # 通用组件
│   │   ├── ui/               # 基础UI组件
│   │   └── features/         # 业务组件
│   │
│   ├── modules/              # 功能模块
│   │   ├── auth/             # 认证模块
│   │   │   ├── api/          # API客户端
│   │   │   ├── hooks/        # 自定义Hooks
│   │   │   └── components/   # 认证相关组件
│   │   │
│   │   └── search/           # 搜索模块
│   │       ├── api/          # API客户端
│   │       ├── hooks/        # 自定义Hooks
│   │       └── components/   # 搜索相关组件
│   │
│   ├── lib/                  # 工具库
│   │   ├── api/              # API基础客户端
│   │   └── utils/            # 工具函数
│   │
│   └── app/                  # Next.js页面
│       ├── page.tsx         # 首页
│       ├── search/          # 搜索页
│       ├── auth/            # 认证页
│       └── dashboard/       # 仪表盘页
```

---

## 4. 接口定义

### 4.1 后端接口规范

#### 4.1.1 认证模块接口

**POST /api/v1/auth/register** - 用户注册
```json
// Request
{
  "email": "user@example.com",
  "username": "username",
  "password": "password123"
}

// Response (201)
{
  "code": 0,
  "message": "注册成功",
  "data": {
    "id": 1,
    "email": "user@example.com",
    "username": "username"
  }
}
```

**POST /api/v1/auth/login** - 用户登录
```json
// Request
{
  "login": "user@example.com",  // 支持邮箱或用户名
  "password": "password123"
}

// Response (200)
{
  "code": 0,
  "message": "登录成功",
  "data": {
    "id": 1,
    "email": "user@example.com",
    "username": "username"
  }
}
// Header: Set-Cookie: token=xxx; HttpOnly; Path=/; Max-Age=604800
```

**POST /api/v1/auth/logout** - 用户登出
```json
// Response (200)
{
  "code": 0,
  "message": "登出成功"
}
// Header: Set-Cookie: token=; HttpOnly; Path=/; Max-Age=0
```

**GET /api/v1/auth/me** - 获取当前用户
```json
// Response (200)
{
  "code": 0,
  "message": "success",
  "data": {
    "id": 1,
    "email": "user@example.com",
    "username": "username",
    "created_at": "2026-05-08T00:00:00Z"
  }
}
```

#### 4.1.2 搜索模块接口

**GET /api/v1/search/github** - GitHub仓库搜索
```json
// Query Parameters
// - q: string (必填) 搜索关键词
// - page: int (可选, 默认1) 页码
// - per_page: int (可选, 默认10) 每页数量

// Response (200)
{
  "code": 0,
  "message": "success",
  "data": {
    "total_count": 1500,
    "page": 1,
    "per_page": 10,
    "items": [
      {
        "id": 123456,
        "name": "facebook/react",
        "full_name": "facebook/react",
        "description": "The library for web and native user interfaces.",
        "html_url": "https://github.com/facebook/react",
        "stargazers_count": 225000,
        "language": "JavaScript",
        "updated_at": "2026-05-08T00:00:00Z"
      }
    ]
  }
}
```

### 4.2 模块间通信协议

#### 4.2.1 服务层 → 数据访问层
使用Repository模式，定义接口协议：

```python
# repository/interfaces.py
from abc import ABC, abstractmethod
from typing import List, Optional

class IUserRepository(ABC):
    @abstractmethod
    async def create(self, user_data: dict) -> dict: pass
    
    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[dict]: pass
    
    @abstractmethod
    async def get_by_username(self, username: str) -> Optional[dict]: pass
    
    @abstractmethod
    async def get_by_id(self, user_id: int) -> Optional[dict]: pass

class ISearchRepository(ABC):
    @abstractmethod
    async def search_github(self, query: str, page: int, per_page: int) -> dict: pass
```

#### 4.2.2 API层 → 服务层
使用Service层解耦：

```python
# services/interfaces.py
from abc import ABC, abstractmethod

class IAuthService(ABC):
    @abstractmethod
    async def register(self, email: str, username: str, password: str) -> dict: pass
    
    @abstractmethod
    async def login(self, login: str, password: str) -> dict: pass
    
    @abstractmethod
    async def get_current_user(self, user_id: int) -> dict: pass

class ISearchService(ABC):
    @abstractmethod
    async def search_github(self, query: str, page: int, per_page: int) -> dict: pass
```

#### 4.2.3 前端 → 后端
使用API客户端封装：

```typescript
// lib/api/client.ts
interface ApiResponse<T> {
  code: number;
  message: string;
  data: T;
}

interface ApiClient {
  get<T>(url: string, params?: Record<string, any>): Promise<ApiResponse<T>>;
  post<T>(url: string, data?: Record<string, any>): Promise<ApiResponse<T>>;
  setToken(token: string): void;
  clearToken(): void;
}
```

---

## 5. 数据库设计

### 5.1 ER图

```
┌─────────────────┐
│     users       │
├─────────────────┤
│ id (PK)         │
│ email (UK)      │
│ username (UK)   │
│ password_hash   │
│ created_at      │
│ updated_at      │
└─────────────────┘
```

### 5.2 表结构

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT users_email_format CHECK (email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'),
    CONSTRAINT users_username_length CHECK (LENGTH(username) >= 3 AND LENGTH(username) <= 100),
    CONSTRAINT users_password_length CHECK (LENGTH(password_hash) >= 60)
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_username ON users(username);
```

---

## 6. 前端页面设计

### 6.1 页面清单

| 页面 | 路由 | 说明 |
|------|------|------|
| 首页 | `/` | 搜索入口 |
| 搜索结果 | `/search?q=xxx` | 搜索结果展示 |
| 注册 | `/auth/register` | 用户注册 |
| 登录 | `/auth/login` | 用户登录 |
| 用户面板 | `/dashboard` | 用户面板（预留空壳） |

### 6.2 页面组件

```
pages/
├── index.tsx              # 首页
├── search/
│   └── page.tsx          # 搜索结果页
├── auth/
│   ├── register/
│   │   └── page.tsx      # 注册页
│   └── login/
│       └── page.tsx      # 登录页
└── dashboard/
    └── page.tsx          # 用户面板

components/
├── layout/
│   ├── Header.tsx         # 页头
│   ├── Footer.tsx         # 页脚
│   └── Layout.tsx         # 布局容器
├── search/
│   ├── SearchBar.tsx      # 搜索框
│   └── SearchResult.tsx   # 搜索结果卡片
└── auth/
    ├── LoginForm.tsx       # 登录表单
    └── RegisterForm.tsx   # 注册表单
```

---

## 7. 项目配置

### 7.1 环境变量

#### 后端 (.env)
```env
# 数据库
DATABASE_URL=postgresql://user:pass@host:5432/onesearch

# JWT
JWT_SECRET_KEY=your-secret-key-here
JWT_ALGORITHM=HS256
JWT_EXPIRATION_DAYS=7

# CORS
CORS_ORIGINS=http://localhost:3000,https://onesearch.vercel.app

# GitHub API
GITHUB_API_TOKEN=ghp_xxx  # 可选，用于提高API限制
```

#### 前端 (.env.local)
```env
NEXT_PUBLIC_API_URL=https://api.onesearch.com
```

### 7.2 依赖清单

#### 后端 (requirements.txt)
```
fastapi==0.109.0
uvicorn[standard]==0.27.0
pydantic==2.5.3
pydantic-settings==2.1.0
sqlalchemy==2.0.25
asyncpg==0.29.0
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6
httpx==0.26.0
```

#### 前端 (package.json)
```json
{
  "dependencies": {
    "next": "14.1.0",
    "react": "18.2.0",
    "react-dom": "18.2.0",
    "@tanstack/react-query": "5.17.0",
    "axios": "1.6.5",
    "zustand": "4.5.0",
    "zod": "3.22.4"
  }
}
```

---

## 8. 开发规范

### 8.1 Git提交规范

```
feat: 新功能
fix: 修复bug
docs: 文档更新
style: 代码格式
refactor: 重构
test: 测试相关
chore: 构建/工具
```

### 8.2 代码风格

- 后端：Black + Ruff
- 前端：ESLint + Prettier

### 8.3 API响应格式

```json
{
  "code": 0,           // 0=成功，非0=失败
  "message": "success", // 消息
  "data": {}           // 数据
}
```

### 8.4 错误码定义

| 错误码 | 说明 |
|--------|------|
| 0 | 成功 |
| 1001 | 参数错误 |
| 1002 | 认证失败 |
| 1003 | 权限不足 |
| 2001 | 用户已存在 |
| 2002 | 用户不存在 |
| 2003 | 密码错误 |
| 3001 | 搜索服务异常 |

---

## 9. 测试策略

### 9.1 后端测试
- 单元测试：pytest + pytest-asyncio
- API测试：FastAPI TestClient

### 9.2 前端测试
- 组件测试：Vitest + React Testing Library
- E2E测试：Playwright

---

## 10. 部署架构

```
┌─────────────────────────────────────────────┐
│                  Vercel                     │
│  ┌───────────────────────────────────────┐  │
│  │           Next.js Frontend            │  │
│  │  - 静态资源/CDN                        │  │
│  │  - SSR页面                             │  │
│  └───────────────────────────────────────┘  │
└─────────────────────────────────────────────┘
                     │
                     │ HTTPS
                     ▼
┌─────────────────────────────────────────────┐
│              Railway / 云服务器              │
│  ┌───────────────────────────────────────┐  │
│  │         FastAPI Backend               │  │
│  │  - API服务                             │  │
│  │  - CORS配置                            │  │
│  └───────────────────────────────────────┘  │
└─────────────────────────────────────────────┘
                     │
                     │ SQL
                     ▼
┌─────────────────────────────────────────────┐
│              Railway PostgreSQL              │
│  ┌───────────────────────────────────────┐  │
│  │           PostgreSQL DB               │  │
│  │  - users表                            │  │
│  └───────────────────────────────────────┘  │
└─────────────────────────────────────────────┘
```

---

## 11. 实施计划

### Phase 1: 项目骨架搭建
1. 初始化前端Next.js项目
2. 初始化后端FastAPI项目
3. 配置Git仓库和CI/CD

### Phase 2: 核心模块开发
1. 后端Core模块（配置、数据库、安全）
2. 前端API客户端封装
3. 前后端联调基础

### Phase 3: 认证模块开发
1. 后端认证API（注册、登录、登出、获取用户）
2. 前端认证页面和表单
3. JWT认证流程

### Phase 4: 搜索模块开发
1. 后端GitHub搜索API
2. 前端搜索页面
3. 结果展示组件

---

## 12. 前端全局配置

### 12.1 全局样式 (globals.css)
```css
@tailwind base;
@tailwind components;
@tailwind utilities;

:root {
  --foreground-rgb: 0, 0, 0;
  --background-start-rgb: 214, 219, 220;
  --background-end-rgb: 255, 255, 255;
}

body {
  color: rgb(var(--foreground-rgb));
  background: linear-gradient(
      to bottom,
      transparent,
      rgb(var(--background-end-rgb))
    )
    rgb(var(--background-start-rgb));
}
```

### 12.2 根组件 (layout.tsx)
```tsx
import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import './globals.css';
import { Providers } from './providers';

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: 'OneSearch 一搜',
  description: '开发者一站式信息搜索工具',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="zh-CN">
      <body className={inter.className}>
        <Providers>{children}</Providers>
      </body>
    </html>
  );
}
```

### 12.3 Providers组件 (providers.tsx)
```tsx
'use client';

import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { useState } from 'react';

export function Providers({ children }: { children: React.ReactNode }) {
  const [queryClient] = useState(
    () =>
      new QueryClient({
        defaultOptions: {
          queries: {
            staleTime: 60 * 1000,
            retry: 1,
          },
        },
      })
  );

  return (
    <QueryClientProvider client={queryClient}>
      {children}
    </QueryClientProvider>
  );
}
```

### 12.4 用户面板 (dashboard/page.tsx)
```tsx
'use client';

import { useAuth } from '@/modules/auth/hooks/useAuth';
import Link from 'next/link';

export default function DashboardPage() {
  const { user, isLoading, logout, isLoggingOut } = useAuth();

  if (isLoading) {
    return <div className="flex justify-center items-center min-h-screen">加载中...</div>;
  }

  if (!user) {
    return (
      <div className="flex justify-center items-center min-h-screen">
        <div className="text-center">
          <p className="mb-4">请先登录</p>
          <Link href="/auth/login" className="text-blue-600 hover:underline">
            前往登录
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-2xl font-bold mb-8">用户面板</h1>
      
      <div className="bg-white shadow rounded-lg p-6">
        <h2 className="text-xl font-semibold mb-4">个人信息</h2>
        <div className="space-y-2">
          <p><span className="text-gray-600">用户名：</span>{user.username}</p>
          <p><span className="text-gray-600">邮箱：</span>{user.email}</p>
          {user.created_at && (
            <p><span className="text-gray-600">注册时间：</span>{new Date(user.created_at).toLocaleString()}</p>
          )}
        </div>
      </div>

      <div className="mt-6">
        <button
          onClick={() => logout()}
          disabled={isLoggingOut}
          className="px-4 py-2 bg-red-500 text-white rounded hover:bg-red-600 disabled:opacity-50"
        >
          {isLoggingOut ? '登出中...' : '退出登录'}
        </button>
      </div>

      <div className="mt-8">
        <h2 className="text-xl font-semibold mb-4">功能预留</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="bg-gray-100 p-4 rounded">
            <h3 className="font-medium">搜索历史</h3>
            <p className="text-gray-500 text-sm mt-1">功能开发中...</p>
          </div>
          <div className="bg-gray-100 p-4 rounded">
            <h3 className="font-medium">收藏夹</h3>
            <p className="text-gray-500 text-sm mt-1">功能开发中...</p>
          </div>
        </div>
      </div>
    </div>
  );
}
```

---

## 13. 容器化配置

### 13.1 后端Dockerfile
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 13.2 docker-compose.yml (可选)
```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://postgres:postgres@db:5432/onesearch
      - JWT_SECRET_KEY=your-secret-key
    depends_on:
      - db

  db:
    image: postgres:15-alpine
    environment:
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres
      - POSTGRES_DB=onesearch
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

---

## 14. 测试配置

### 14.1 后端pytest配置 (pytest.ini)
```ini
[pytest]
asyncio_mode = auto
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = -v --tb=short
```

### 14.2 后端测试示例 (tests/test_auth.py)
```python
import pytest
from httpx import AsyncClient
from app.main import app


@pytest.mark.asyncio
async def test_health_check():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"
```

### 14.3 前端Vitest配置 (vitest.config.ts)
```typescript
import { defineConfig } from 'vitest/config';
import react from '@vitejs/plugin-react';
import path from 'path';

export default defineConfig({
  plugins: [react()],
  test: {
    environment: 'jsdom',
    globals: true,
  },
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
});
```

---

## 15. README模板

### 15.1 项目README (README.md)
```markdown
# OneSearch 一搜

开发者一站式信息搜索工具

## 技术栈

- **前端**: Next.js 14, React 18, TypeScript, TailwindCSS
- **后端**: Python, FastAPI, SQLAlchemy
- **数据库**: PostgreSQL
- **认证**: JWT + HTTP Only Cookie

## 快速开始

### 前端

\`\`\`bash
cd frontend
npm install
npm run dev
\`\`\`

### 后端

\`\`\`bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
\`\`\`

## 环境变量

### 后端 (.env)
\`\`\`env
DATABASE_URL=postgresql://user:password@localhost:5432/onesearch
JWT_SECRET_KEY=your-secret-key
CORS_ORIGINS=http://localhost:3000
\`\`\`

### 前端 (.env.local)
\`\`\`env
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
\`\`\`

## API文档

启动后端后访问: http://localhost:8000/docs
```

---

**文档状态：** 待实施
**最后更新：** 2026-05-08
