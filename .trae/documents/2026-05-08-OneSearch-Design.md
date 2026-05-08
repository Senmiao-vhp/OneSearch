# OneSearch 一搜 - 产品设计文档

**版本：** v1.0  
**日期：** 2026-05-08  
**状态：** 待用户确认

---

## 1. 项目概述

### 1.1 项目定位
开发者一站式信息搜索工具

### 1.2 核心价值
整合CSDN技术博客、知网学术论文、GitHub/Gitee代码仓库四大数据源，提供一站式搜索体验。解决开发者搜资料需频繁切换网站的痛点，将原本需要打开多个网站的搜索流程简化为一次输入。

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

### 2.2 系统架构

```
┌─────────────────────────────────────────────────────────────┐
│                        用户浏览器                             │
└─────────────────────────┬───────────────────────────────────┘
                          │ HTTPS
┌─────────────────────────▼───────────────────────────────────┐
│                      Vercel (Next.js)                        │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │   首页/搜索   │  │   用户系统   │  │     用户面板          │  │
│  │   搜索结果    │  │  注册/登录   │  │    (预留空壳)         │  │
│  └─────────────┘  └─────────────┘  └─────────────────────┘  │
└─────────────────────────┬───────────────────────────────────┘
                          │ API请求 (HTTPS)
┌─────────────────────────▼───────────────────────────────────┐
│                   Railway (FastAPI)                          │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │  认证模块    │  │  搜索模块    │  │   GitHub API集成    │  │
│  │  注册/登录   │  │  结果聚合    │  │                     │  │
│  └──────┬──────┘  └─────────────┘  └─────────────────────┘  │
└─────────┼───────────────────────────────────────────────────┘
          │
┌─────────▼───────────────────────────────────────────────────┐
│                    Railway (PostgreSQL)                       │
│  ┌─────────────┐                                             │
│  │   用户表    │                                             │
│  │  users      │                                             │
│  └─────────────┘                                             │
└─────────────────────────────────────────────────────────────┘
```

### 2.3 数据模型

#### 用户表 (users)
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## 3. 功能模块

### 3.1 用户系统 (MVP)

#### 注册功能
- 输入：邮箱、用户名、密码
- 验证：邮箱格式、密码强度（≥8位）
- 返回：注册成功/失败信息

#### 登录功能
- 输入：邮箱/用户名 + 密码
- 返回：JWT Token（HTTP Only Cookie）
- 有效期：7天

#### 用户面板
- 预留空壳页面
- 后续扩展：搜索历史、收藏夹

### 3.2 搜索功能 (MVP)

#### 搜索入口
- 关键词输入框
- 搜索按钮/回车触发

#### GitHub搜索
- 调用GitHub REST API
- 搜索范围：仓库名称、描述、README
- 返回：仓库列表（名称、描述、星标数、链接）

#### 结果展示
- 卡片式列表
- 显示：仓库名、描述、星标数、编程语言
- 一键跳转GitHub

---

## 4. API设计

### 4.1 认证接口

| 方法 | 路径 | 描述 |
|------|------|------|
| POST | `/api/auth/register` | 用户注册 |
| POST | `/api/auth/login` | 用户登录 |
| POST | `/api/auth/logout` | 用户登出 |
| GET | `/api/auth/me` | 获取当前用户 |

### 4.2 搜索接口

| 方法 | 路径 | 描述 |
|------|------|------|
| GET | `/api/search/github` | GitHub仓库搜索 |

#### 请求示例
```
GET /api/search/github?q=react&page=1&per_page=10
```

#### 响应示例
```json
{
  "success": true,
  "data": {
    "total_count": 1500,
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

---

## 5. 前端页面

### 5.1 页面列表

| 页面 | 路由 | 描述 |
|------|------|------|
| 首页 | `/` | 搜索入口 |
| 搜索结果 | `/search` | GitHub搜索结果 |
| 注册 | `/auth/register` | 用户注册 |
| 登录 | `/auth/login` | 用户登录 |
| 用户面板 | `/dashboard` | 用户面板（预留） |

### 5.2 首页设计
- Logo + 项目名称
- 搜索输入框（大号）
- 搜索按钮
- 简洁科技风UI

---

## 6. 后续扩展 (非MVP)

### 6.1 数据源扩展
- CSDN技术博客爬虫
- 知网学术论文爬虫
- Gitee代码仓库

### 6.2 功能扩展
- 搜索历史记录
- 收藏夹功能
- 多平台聚合排序
- 代码片段预览

---

## 7. 项目结构

### 7.1 前端 (Next.js)
```
frontend/
├── src/
│   ├── app/              # Next.js App Router
│   │   ├── page.tsx      # 首页
│   │   ├── search/       # 搜索结果页
│   │   ├── auth/         # 认证页面
│   │   └── dashboard/    # 用户面板
│   ├── components/       # 组件
│   ├── lib/             # 工具函数
│   └── styles/          # 样式
├── package.json
└── next.config.js
```

### 7.2 后端 (FastAPI)
```
backend/
├── app/
│   ├── api/             # API路由
│   │   ├── auth.py      # 认证接口
│   │   └── search.py    # 搜索接口
│   ├── core/            # 核心配置
│   │   ├── config.py    # 配置
│   │   ├── security.py  # 安全/JWT
│   │   └── database.py  # 数据库连接
│   ├── models/         # 数据模型
│   ├── schemas/        # Pydantic模型
│   └── main.py         # 应用入口
├── requirements.txt
└── Dockerfile
```

---

## 8. 安全考虑

- 密码bcrypt加密存储
- JWT Token使用HTTP Only Cookie
- CORS配置限制
- 输入参数校验
- SQL注入防护（ORM）
- API限流（后续添加）

---

## 9. 决策总结

| 决策项 | 选择 |
|--------|------|
| 项目名称 | OneSearch（一搜） |
| 前端框架 | Next.js |
| 后端框架 | Python + FastAPI |
| 数据库 | PostgreSQL |
| 认证方式 | HTTP Only Cookie + JWT |
| 部署方式 | 前后端分离 |
| MVP功能 | 用户系统 + GitHub搜索 |
| MVP后端 | Railway |
| MVP前端 | Vercel |
