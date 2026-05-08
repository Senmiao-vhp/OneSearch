# OneSearch 实施计划

> **目标：** 搭建系统框架，完成所有模块的接口声明（不含具体业务逻辑）

**架构概述：** 
前后端分离架构，前端Next.js部署Vercel，后端FastAPI部署Railway，PostgreSQL存储用户数据。模块间通过清晰接口协议通信，支持并行开发。

**技术栈：**
- 前端：Next.js 14, React 18, TypeScript, Axios, React Query, Zustand
- 后端：FastAPI, Python 3.11+, SQLAlchemy, PostgreSQL, JWT

---

## 模块划分与依赖关系

```
Phase 1: 基础架构（可并行）
├── 1.1 前端项目初始化
├── 1.2 后端项目初始化
└── 1.3 数据库配置

Phase 2: 核心模块（1.1完成后）
├── 2.1 后端Core模块
└── 2.2 前端API客户端

Phase 3: 认证模块（2.1, 2.2完成后）
├── 3.1 后端认证API（接口声明+Mock）
├── 3.2 前端认证页面
└── 3.3 认证流程串联

Phase 4: 搜索模块（2.1, 2.2完成后）
├── 4.1 后端搜索API（接口声明+Mock）
├── 4.2 前端搜索页面
└── 4.3 搜索流程串联
```

---

## Phase 1: 基础架构

### Task 1.1: 前端项目初始化

**文件：**
- 创建: `frontend/package.json`
- 创建: `frontend/tsconfig.json`
- 创建: `frontend/next.config.js`
- 创建: `frontend/.env.local`
- 创建: `frontend/.gitignore`

**步骤：**

- [ ] **Step 1: 创建 package.json**

```json
{
  "name": "onesearch-frontend",
  "version": "0.1.0",
  "private": true,
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "next lint",
    "type-check": "tsc --noEmit"
  },
  "dependencies": {
    "next": "14.1.0",
    "react": "18.2.0",
    "react-dom": "18.2.0",
    "@tanstack/react-query": "5.17.0",
    "axios": "1.6.5",
    "zustand": "4.5.0",
    "zod": "3.22.4"
  },
  "devDependencies": {
    "@types/node": "20.11.0",
    "@types/react": "18.2.48",
    "@types/react-dom": "18.2.18",
    "typescript": "5.3.3",
    "eslint": "8.56.0",
    "eslint-config-next": "14.1.0"
  }
}
```

- [ ] **Step 2: 创建 tsconfig.json**

```json
{
  "compilerOptions": {
    "target": "ES2017",
    "lib": ["dom", "dom.iterable", "esnext"],
    "allowJs": true,
    "skipLibCheck": true,
    "strict": true,
    "noEmit": true,
    "esModuleInterop": true,
    "module": "esnext",
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "jsx": "preserve",
    "incremental": true,
    "plugins": [{ "name": "next" }],
    "paths": {
      "@/*": ["./src/*"]
    }
  },
  "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx", ".next/types/**/*.ts"],
  "exclude": ["node_modules"]
}
```

- [ ] **Step 3: 创建 next.config.js**

```javascript
/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
  },
};

module.exports = nextConfig;
```

- [ ] **Step 4: 创建 .env.local**

```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
```

- [ ] **Step 5: 创建 .gitignore**

```
# dependencies
/node_modules
/.pnp
.pnp.js

# testing
/coverage

# next.js
/.next/
/out/

# production
/build

# misc
.DS_Store
*.pem

# debug
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# local env files
.env*.local

# vercel
.vercel

# typescript
*.tsbuildinfo
next-env.d.ts
```

- [ ] **Step 6: 创建基础目录结构**

创建以下目录：
- `frontend/src/app/` - Next.js App Router
- `frontend/src/components/` - 组件目录
- `frontend/src/lib/` - 工具库
- `frontend/src/types/` - TypeScript类型定义

---

### Task 1.2: 后端项目初始化

**文件：**
- 创建: `backend/requirements.txt`
- 创建: `backend/.env.example`
- 创建: `backend/.gitignore`
- 创建: `backend/app/__init__.py`
- 创建: `backend/app/main.py`

**步骤：**

- [ ] **Step 1: 创建 requirements.txt**

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
psycopg2-binary==2.9.9
alembic==1.13.1
```

- [ ] **Step 2: 创建 .env.example**

```env
# 数据库
DATABASE_URL=postgresql://user:password@localhost:5432/onesearch

# JWT配置
JWT_SECRET_KEY=your-secret-key-change-in-production
JWT_ALGORITHM=HS256
JWT_EXPIRATION_MINUTES=10080

# CORS配置
CORS_ORIGINS=http://localhost:3000,https://onesearch.vercel.app

# GitHub API Token (可选)
GITHUB_API_TOKEN=
```

- [ ] **Step 3: 创建 .gitignore**

```
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

.env
.venv
env/
venv/
ENV/

.pytest_cache/
.coverage
htmlcov/

migrations/
*.db
*.sqlite3

.DS_Store
.idea/
.vscode/
*.swp
*.swo
```

- [ ] **Step 4: 创建目录结构**

创建以下目录：
- `backend/app/core/` - 核心配置
- `backend/app/modules/` - 功能模块
- `backend/app/shared/` - 共享模块
- `backend/tests/` - 测试目录

创建 `__init__.py` 文件：
- `backend/app/__init__.py`
- `backend/app/core/__init__.py`
- `backend/app/modules/__init__.py`
- `backend/app/shared/__init__.py`

- [ ] **Step 5: 创建 main.py**

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings


def create_app() -> FastAPI:
    app = FastAPI(
        title="OneSearch API",
        description="开发者一站式信息搜索工具 API",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
    )
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    return app


app = create_app()


@app.get("/")
async def root():
    return {"message": "OneSearch API", "version": "1.0.0"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
```

---

### Task 1.3: 数据库配置

**文件：**
- 创建: `backend/app/core/config.py`
- 创建: `backend/app/core/database.py`
- 创建: `backend/app/shared/models/base.py`
- 创建: `backend/migrations/env.py`

**步骤：**

- [ ] **Step 1: 创建 config.py**

```python
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    PROJECT_NAME: str = "OneSearch"
    VERSION: str = "1.0.0"
    
    # 数据库
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/onesearch"
    
    # JWT
    JWT_SECRET_KEY: str = "your-secret-key-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_MINUTES: int = 10080
    
    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000"]
    
    # GitHub API
    GITHUB_API_TOKEN: str = ""
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
```

- [ ] **Step 2: 创建 database.py**

```python
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from app.core.config import settings


engine = create_async_engine(
    settings.DATABASE_URL,
    echo=False,
    future=True,
)

AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

Base = declarative_base()


async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
```

- [ ] **Step 3: 创建用户模型 users.py**

```python
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.core.database import Base


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    username = Column(String(100), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
```

- [ ] **Step 4: 创建数据库迁移配置**

使用Alembic管理数据库迁移：
- 创建 `backend/alembic.ini`
- 创建 `backend/migrations/env.py`

```bash
# 在 backend 目录执行
alembic init migrations
```

---

## Phase 2: 核心模块

### Task 2.1: 后端Core模块

**文件：**
- 创建: `backend/app/core/exceptions.py`
- 创建: `backend/app/core/security.py`
- 创建: `backend/app/shared/dependencies.py`
- 创建: `backend/app/shared/schemas/base.py`

**步骤：**

- [ ] **Step 1: 创建 exceptions.py**

```python
from fastapi import HTTPException, status


class AppException(HTTPException):
    def __init__(self, code: int, message: str, status_code: int = status.HTTP_400_BAD_REQUEST):
        self.code = code
        self.message = message
        super().__init__(status_code=status_code, detail=message)


class UnauthorizedException(AppException):
    def __init__(self, message: str = "认证失败"):
        super().__init__(code=1002, message=message, status_code=status.HTTP_401_UNAUTHORIZED)


class ForbiddenException(AppException):
    def __init__(self, message: str = "权限不足"):
        super().__init__(code=1003, message=message, status_code=status.HTTP_403_FORBIDDEN)


class NotFoundException(AppException):
    def __init__(self, message: str = "资源不存在"):
        super().__init__(code=404, message=message, status_code=status.HTTP_404_NOT_FOUND)


class UserAlreadyExistsException(AppException):
    def __init__(self, message: str = "用户已存在"):
        super().__init__(code=2001, message=message, status_code=status.HTTP_409_CONFLICT)


class InvalidCredentialsException(AppException):
    def __init__(self, message: str = "用户名或密码错误"):
        super().__init__(code=2003, message=message, status_code=status.HTTP_401_UNAUTHORIZED)
```

- [ ] **Step 2: 创建 security.py**

```python
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.core.config import settings


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.JWT_EXPIRATION_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> Optional[dict]:
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        return payload
    except JWTError:
        return None
```

- [ ] **Step 3: 创建 base.py (响应模型)**

```python
from pydantic import BaseModel
from typing import Generic, TypeVar, Optional

T = TypeVar("T")


class ResponseBase(BaseModel):
    code: int = 0
    message: str = "success"


class DataResponse(ResponseBase, Generic[T]):
    data: Optional[T] = None


class ListResponse(ResponseBase, Generic[T]):
    data: Optional[T] = None
    total: int = 0
    page: int = 1
    per_page: int = 10
```

- [ ] **Step 4: 创建 dependencies.py**

```python
from fastapi import Depends, Cookie, Request
from typing import Optional
from app.core.security import decode_access_token
from app.core.exceptions import UnauthorizedException


async def get_current_user_id(token: Optional[str] = Cookie(None)) -> int:
    if not token:
        raise UnauthorizedException("未登录")
    
    payload = decode_access_token(token)
    if not payload:
        raise UnauthorizedException("Token无效")
    
    user_id = payload.get("sub")
    if not user_id:
        raise UnauthorizedException("Token无效")
    
    return int(user_id)


def get_optional_user_id(token: Optional[str] = Cookie(None)) -> Optional[int]:
    if not token:
        return None
    
    payload = decode_access_token(token)
    if not payload:
        return None
    
    user_id = payload.get("sub")
    if not user_id:
        return None
    
    return int(user_id)
```

---

### Task 2.2: 前端API客户端

**文件：**
- 创建: `frontend/src/lib/api/client.ts`
- 创建: `frontend/src/lib/api/types.ts`
- 创建: `frontend/src/types/api.ts`

**步骤：**

- [ ] **Step 1: 创建 api/types.ts**

```typescript
export interface ApiResponse<T = any> {
  code: number;
  message: string;
  data: T;
}

export interface User {
  id: number;
  email: string;
  username: string;
  created_at?: string;
}

export interface RegisterRequest {
  email: string;
  username: string;
  password: string;
}

export interface LoginRequest {
  login: string;
  password: string;
}

export interface GithubSearchItem {
  id: number;
  name: string;
  full_name: string;
  description: string | null;
  html_url: string;
  stargazers_count: number;
  language: string | null;
  updated_at: string;
}

export interface GithubSearchResponse {
  total_count: number;
  page: number;
  per_page: number;
  items: GithubSearchItem[];
}
```

- [ ] **Step 2: 创建 api/client.ts**

```typescript
import axios, { AxiosInstance, AxiosError } from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

class ApiClient {
  private client: AxiosInstance;

  constructor() {
    this.client = axios.create({
      baseURL: API_BASE_URL,
      timeout: 30000,
      headers: {
        'Content-Type': 'application/json',
      },
      withCredentials: true,
    });

    this.client.interceptors.response.use(
      (response) => response,
      (error: AxiosError) => {
        const message = (error.response?.data as any)?.message || error.message;
        return Promise.reject(new Error(message));
      }
    );
  }

  async get<T>(url: string, params?: Record<string, any>): Promise<T> {
    const response = await this.client.get<T>(url, { params });
    return response.data;
  }

  async post<T>(url: string, data?: Record<string, any>): Promise<T> {
    const response = await this.client.post<T>(url, data);
    return response.data;
  }

  async put<T>(url: string, data?: Record<string, any>): Promise<T> {
    const response = await this.client.put<T>(url, data);
    return response.data;
  }

  async delete<T>(url: string): Promise<T> {
    const response = await this.client.delete<T>(url);
    return response.data;
  }
}

export const apiClient = new ApiClient();
```

- [ ] **Step 3: 创建 auth API客户端**

```typescript
import { apiClient } from './client';
import { ApiResponse, User, RegisterRequest, LoginRequest } from './types';

export const authApi = {
  register: async (data: RegisterRequest): Promise<ApiResponse<User>> => {
    return apiClient.post('/auth/register', data);
  },

  login: async (data: LoginRequest): Promise<ApiResponse<User>> => {
    return apiClient.post('/auth/login', data);
  },

  logout: async (): Promise<ApiResponse<null>> => {
    return apiClient.post('/auth/logout');
  },

  getCurrentUser: async (): Promise<ApiResponse<User>> => {
    return apiClient.get('/auth/me');
  },
};
```

- [ ] **Step 4: 创建 search API客户端**

```typescript
import { apiClient } from './client';
import { ApiResponse, GithubSearchResponse } from './types';

export interface SearchParams {
  q: string;
  page?: number;
  per_page?: number;
}

export const searchApi = {
  searchGithub: async (params: SearchParams): Promise<ApiResponse<GithubSearchResponse>> => {
    return apiClient.get('/search/github', params);
  },
};
```

---

## Phase 3: 认证模块

### Task 3.1: 后端认证API

**文件：**
- 创建: `backend/app/modules/auth/schemas/request.py`
- 创建: `backend/app/modules/auth/schemas/response.py`
- 创建: `backend/app/modules/auth/api/endpoints.py`
- 创建: `backend/app/modules/auth/services/interfaces.py`
- 创建: `backend/app/modules/auth/services/auth_service.py`
- 创建: `backend/app/modules/auth/repository/interfaces.py`
- 创建: `backend/app/modules/auth/repository/user_repository.py`
- 修改: `backend/app/main.py` (注册路由)

**步骤：**

- [ ] **Step 1: 创建请求模型 request.py**

```python
from pydantic import BaseModel, EmailStr, Field


class RegisterRequest(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=100)
    password: str = Field(..., min_length=8, max_length=100)


class LoginRequest(BaseModel):
    login: str = Field(..., min_length=1)
    password: str = Field(..., min_length=1)
```

- [ ] **Step 2: 创建响应模型 response.py**

```python
from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class UserResponse(BaseModel):
    id: int
    email: str
    username: str
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class MessageResponse(BaseModel):
    message: str
```

- [ ] **Step 3: 创建Repository接口**

```python
from abc import ABC, abstractmethod
from typing import Optional
from app.modules.auth.schemas.request import RegisterRequest


class IUserRepository(ABC):
    @abstractmethod
    async def create(self, user_data: RegisterRequest, password_hash: str) -> dict:
        pass

    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[dict]:
        pass

    @abstractmethod
    async def get_by_username(self, username: str) -> Optional[dict]:
        pass

    @abstractmethod
    async def get_by_id(self, user_id: int) -> Optional[dict]:
        pass

    @abstractmethod
    async def get_by_email_or_username(self, login: str) -> Optional[dict]:
        pass
```

- [ ] **Step 4: 创建Repository实现**

```python
from typing import Optional
from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import AsyncSessionLocal
from app.modules.auth.schemas.request import RegisterRequest
from app.modules.auth.repository.interfaces import IUserRepository
from app.shared.models.users import User


class UserRepository(IUserRepository):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, user_data: RegisterRequest, password_hash: str) -> dict:
        # TODO: 实现用户创建
        pass

    async def get_by_email(self, email: str) -> Optional[dict]:
        # TODO: 实现根据邮箱查询
        pass

    async def get_by_username(self, username: str) -> Optional[dict]:
        # TODO: 实现根据用户名查询
        pass

    async def get_by_id(self, user_id: int) -> Optional[dict]:
        # TODO: 实现根据ID查询
        pass

    async def get_by_email_or_username(self, login: str) -> Optional[dict]:
        # TODO: 实现根据邮箱或用户名查询
        pass
```

- [ ] **Step 5: 创建Service接口**

```python
from abc import ABC, abstractmethod
from typing import Optional


class IAuthService(ABC):
    @abstractmethod
    async def register(self, email: str, username: str, password: str) -> dict:
        pass

    @abstractmethod
    async def login(self, login: str, password: str) -> dict:
        pass

    @abstractmethod
    async def get_current_user(self, user_id: int) -> Optional[dict]:
        pass

    @abstractmethod
    async def logout(self) -> dict:
        pass
```

- [ ] **Step 6: 创建Service实现**

```python
from typing import Optional
from app.modules.auth.services.interfaces import IAuthService
from app.modules.auth.repository.interfaces import IUserRepository
from app.core.security import get_password_hash, verify_password, create_access_token
from app.core.exceptions import UserAlreadyExistsException, InvalidCredentialsException, NotFoundException


class AuthService(IAuthService):
    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository

    async def register(self, email: str, username: str, password: str) -> dict:
        # TODO: 实现注册逻辑
        # 1. 检查邮箱是否存在
        # 2. 检查用户名是否存在
        # 3. 加密密码
        # 4. 创建用户
        pass

    async def login(self, login: str, password: str) -> dict:
        # TODO: 实现登录逻辑
        # 1. 根据邮箱或用户名查询用户
        # 2. 验证密码
        # 3. 生成JWT Token
        pass

    async def get_current_user(self, user_id: int) -> Optional[dict]:
        # TODO: 实现获取当前用户逻辑
        pass

    async def logout(self) -> dict:
        # TODO: 实现登出逻辑（JWT无状态，客户端删除cookie即可）
        return {"message": "登出成功"}
```

- [ ] **Step 7: 创建API路由 endpoints.py**

```python
from fastapi import APIRouter, Depends, Response
from app.modules.auth.schemas.request import RegisterRequest, LoginRequest
from app.modules.auth.schemas.response import UserResponse, MessageResponse
from app.modules.auth.services.auth_service import AuthService
from app.modules.auth.repository.user_repository import UserRepository
from app.shared.dependencies import get_db, get_current_user_id
from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter(prefix="/auth", tags=["认证"])


def get_auth_service(db: AsyncSession = Depends(get_db)) -> AuthService:
    return AuthService(UserRepository(db))


@router.post("/register", response_model=UserResponse, status_code=201)
async def register(
    request: RegisterRequest,
    response: Response,
    service: AuthService = Depends(get_auth_service),
):
    # TODO: 调用service.register()
    pass


@router.post("/login", response_model=UserResponse)
async def login(
    request: LoginRequest,
    response: Response,
    service: AuthService = Depends(get_auth_service),
):
    # TODO: 调用service.login()
    # 设置HTTP Only Cookie
    pass


@router.post("/logout", response_model=MessageResponse)
async def logout(response: Response):
    # TODO: 清除Cookie
    pass


@router.get("/me", response_model=UserResponse)
async def get_current_user(
    user_id: int = Depends(get_current_user_id),
    service: AuthService = Depends(get_auth_service),
):
    # TODO: 调用service.get_current_user()
    pass
```

- [ ] **Step 8: 注册路由到main.py**

```python
from app.modules.auth.api.endpoints import router as auth_router

app.include_router(auth_router, prefix="/api/v1")
```

---

### Task 3.2: 前端认证页面

**文件：**
- 创建: `frontend/src/components/auth/LoginForm.tsx`
- 创建: `frontend/src/components/auth/RegisterForm.tsx`
- 创建: `frontend/src/app/auth/login/page.tsx`
- 创建: `frontend/src/app/auth/register/page.tsx`
- 创建: `frontend/src/modules/auth/hooks/useAuth.ts`
- 创建: `frontend/src/modules/auth/store/authStore.ts`

**步骤：**

- [ ] **Step 1: 创建认证Store**

```typescript
import { create } from 'zustand';
import { User } from '@/lib/api/types';

interface AuthState {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  setUser: (user: User | null) => void;
  setLoading: (loading: boolean) => void;
  logout: () => void;
}

export const useAuthStore = create<AuthState>((set) => ({
  user: null,
  isAuthenticated: false,
  isLoading: true,
  setUser: (user) => set({ user, isAuthenticated: !!user }),
  setLoading: (isLoading) => set({ isLoading }),
  logout: () => set({ user: null, isAuthenticated: false }),
}));
```

- [ ] **Step 2: 创建useAuth Hook**

```typescript
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { authApi } from '@/lib/api/auth';
import { useAuthStore } from '../store/authStore';
import { useRouter } from 'next/navigation';

export function useAuth() {
  const { setUser, setLoading, isAuthenticated } = useAuthStore();
  const router = useRouter();
  const queryClient = useQueryClient();

  const { data: currentUser, isLoading: isLoadingUser } = useQuery({
    queryKey: ['currentUser'],
    queryFn: async () => {
      const response = await authApi.getCurrentUser();
      if (response.code === 0) {
        return response.data;
      }
      return null;
    },
    retry: false,
    onSuccess: (data) => {
      setUser(data);
      setLoading(false);
    },
    onError: () => {
      setUser(null);
      setLoading(false);
    },
  });

  const registerMutation = useMutation({
    mutationFn: authApi.register,
    onSuccess: (response) => {
      if (response.code === 0) {
        setUser(response.data);
        router.push('/');
      }
    },
  });

  const loginMutation = useMutation({
    mutationFn: authApi.login,
    onSuccess: (response) => {
      if (response.code === 0) {
        setUser(response.data);
        router.push('/');
      }
    },
  });

  const logoutMutation = useMutation({
    mutationFn: authApi.logout,
    onSuccess: () => {
      setUser(null);
      queryClient.clear();
      router.push('/auth/login');
    },
  });

  return {
    user: currentUser,
    isAuthenticated,
    isLoading: isLoadingUser,
    register: registerMutation.mutateAsync,
    login: loginMutation.mutateAsync,
    logout: logoutMutation.mutateAsync,
    isRegistering: registerMutation.isPending,
    isLoggingIn: loginMutation.isPending,
    isLoggingOut: logoutMutation.isPending,
  };
}
```

- [ ] **Step 3: 创建LoginForm组件**

```tsx
'use client';

import { useState } from 'react';
import { useAuth } from '@/modules/auth/hooks/useAuth';

export function LoginForm() {
  const [login, setLogin] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const { login: doLogin, isLoggingIn } = useAuth();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    try {
      await doLogin({ login, password });
    } catch (err: any) {
      setError(err.message || '登录失败');
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      {error && <div className="text-red-500">{error}</div>}
      <div>
        <label htmlFor="login">邮箱/用户名</label>
        <input
          id="login"
          type="text"
          value={login}
          onChange={(e) => setLogin(e.target.value)}
          required
        />
      </div>
      <div>
        <label htmlFor="password">密码</label>
        <input
          id="password"
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
      </div>
      <button type="submit" disabled={isLoggingIn}>
        {isLoggingIn ? '登录中...' : '登录'}
      </button>
    </form>
  );
}
```

- [ ] **Step 4: 创建RegisterForm组件**

```tsx
'use client';

import { useState } from 'react';
import { useAuth } from '@/modules/auth/hooks/useAuth';

export function RegisterForm() {
  const [email, setEmail] = useState('');
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [error, setError] = useState('');
  const { register, isRegistering } = useAuth();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    
    if (password !== confirmPassword) {
      setError('两次密码输入不一致');
      return;
    }
    
    try {
      await register({ email, username, password });
    } catch (err: any) {
      setError(err.message || '注册失败');
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      {error && <div className="text-red-500">{error}</div>}
      <div>
        <label htmlFor="email">邮箱</label>
        <input
          id="email"
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />
      </div>
      <div>
        <label htmlFor="username">用户名</label>
        <input
          id="username"
          type="text"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          required
        />
      </div>
      <div>
        <label htmlFor="password">密码</label>
        <input
          id="password"
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
          minLength={8}
        />
      </div>
      <div>
        <label htmlFor="confirmPassword">确认密码</label>
        <input
          id="confirmPassword"
          type="password"
          value={confirmPassword}
          onChange={(e) => setConfirmPassword(e.target.value)}
          required
          minLength={8}
        />
      </div>
      <button type="submit" disabled={isRegistering}>
        {isRegistering ? '注册中...' : '注册'}
      </button>
    </form>
  );
}
```

- [ ] **Step 5: 创建登录页面**

```tsx
'use client';

import { LoginForm } from '@/components/auth/LoginForm';
import Link from 'next/link';

export default function LoginPage() {
  return (
    <div className="min-h-screen flex items-center justify-center">
      <div className="w-full max-w-md p-8">
        <h1>登录 OneSearch</h1>
        <LoginForm />
        <p className="mt-4 text-center">
          还没有账号? <Link href="/auth/register">立即注册</Link>
        </p>
      </div>
    </div>
  );
}
```

- [ ] **Step 6: 创建注册页面**

```tsx
'use client';

import { RegisterForm } from '@/components/auth/RegisterForm';
import Link from 'next/link';

export default function RegisterPage() {
  return (
    <div className="min-h-screen flex items-center justify-center">
      <div className="w-full max-w-md p-8">
        <h1>注册 OneSearch</h1>
        <RegisterForm />
        <p className="mt-4 text-center">
          已有账号? <Link href="/auth/login">立即登录</Link>
        </p>
      </div>
    </div>
  );
}
```

---

## Phase 4: 搜索模块

### Task 4.1: 后端搜索API

**文件：**
- 创建: `backend/app/modules/search/schemas/response.py`
- 创建: `backend/app/modules/search/api/endpoints.py`
- 创建: `backend/app/modules/search/services/interfaces.py`
- 创建: `backend/app/modules/search/services/search_service.py`
- 创建: `backend/app/modules/search/integrations/interfaces.py`
- 创建: `backend/app/modules/search/integrations/github_integration.py`
- 修改: `backend/app/main.py` (注册搜索路由)

**步骤：**

- [ ] **Step 1: 创建响应模型 response.py**

```python
from pydantic import BaseModel
from typing import List, Optional


class GithubRepoItem(BaseModel):
    id: int
    name: str
    full_name: str
    description: Optional[str] = None
    html_url: str
    stargazers_count: int
    language: Optional[str] = None
    updated_at: str

    class Config:
        from_attributes = True


class GithubSearchResponse(BaseModel):
    total_count: int
    page: int
    per_page: int
    items: List[GithubRepoItem]
```

- [ ] **Step 2: 创建集成接口**

```python
from abc import ABC, abstractmethod
from typing import List


class IGitHubIntegration(ABC):
    @abstractmethod
    async def search_repositories(
        self, 
        query: str, 
        page: int = 1, 
        per_page: int = 10
    ) -> dict:
        pass
```

- [ ] **Step 3: 创建GitHub集成实现**

```python
from typing import List, Optional
import httpx
from app.modules.search.integrations.interfaces import IGitHubIntegration
from app.modules.search.schemas.response import GithubRepoItem
from app.core.config import settings


class GitHubIntegration(IGitHubIntegration):
    def __init__(self):
        self.base_url = "https://api.github.com"
        self.headers = {
            "Accept": "application/vnd.github.v3+json",
        }
        if settings.GITHUB_API_TOKEN:
            self.headers["Authorization"] = f"token {settings.GITHUB_API_TOKEN}"

    async def search_repositories(
        self, 
        query: str, 
        page: int = 1, 
        per_page: int = 10
    ) -> dict:
        # TODO: 实现GitHub API调用
        # 使用httpx异步请求GitHub Search API
        # URL: GET /search/repositories?q={query}&page={page}&per_page={per_page}
        pass
```

- [ ] **Step 4: 创建Service接口**

```python
from abc import ABC, abstractmethod


class ISearchService(ABC):
    @abstractmethod
    async def search_github(self, query: str, page: int, per_page: int) -> dict:
        pass
```

- [ ] **Step 5: 创建Service实现**

```python
from app.modules.search.services.interfaces import ISearchService
from app.modules.search.integrations.interfaces import IGitHubIntegration


class SearchService(ISearchService):
    def __init__(self, github_integration: IGitHubIntegration):
        self.github_integration = github_integration

    async def search_github(self, query: str, page: int, per_page: int) -> dict:
        # TODO: 实现搜索逻辑
        # 调用github_integration.search_repositories()
        pass
```

- [ ] **Step 6: 创建API路由 endpoints.py**

```python
from fastapi import APIRouter, Depends, Query
from app.modules.search.schemas.response import GithubSearchResponse
from app.modules.search.services.search_service import SearchService
from app.modules.search.integrations.github_integration import GitHubIntegration


router = APIRouter(prefix="/search", tags=["搜索"])


def get_search_service() -> SearchService:
    return SearchService(GitHubIntegration())


@router.get("/github", response_model=GithubSearchResponse)
async def search_github(
    q: str = Query(..., description="搜索关键词"),
    page: int = Query(1, ge=1, description="页码"),
    per_page: int = Query(10, ge=1, le=100, description="每页数量"),
    service: SearchService = Depends(get_search_service),
):
    # TODO: 调用service.search_github()
    pass
```

- [ ] **Step 7: 注册路由到main.py**

```python
from app.modules.search.api.endpoints import router as search_router

app.include_router(search_router, prefix="/api/v1")
```

---

### Task 4.2: 前端搜索页面

**文件：**
- 创建: `frontend/src/components/search/SearchBar.tsx`
- 创建: `frontend/src/components/search/SearchResultCard.tsx`
- 创建: `frontend/src/components/search/SearchResultList.tsx`
- 创建: `frontend/src/modules/search/hooks/useSearch.ts`
- 创建: `frontend/src/app/search/page.tsx`
- 创建: `frontend/src/app/page.tsx` (首页)

**步骤：**

- [ ] **Step 1: 创建useSearch Hook**

```typescript
import { useQuery } from '@tanstack/react-query';
import { searchApi, SearchParams } from '@/lib/api/search';
import { useSearchParams } from 'next/navigation';

export function useSearch() {
  const searchParams = useSearchParams();
  const query = searchParams.get('q') || '';
  const page = parseInt(searchParams.get('page') || '1');

  const { data, isLoading, error, refetch } = useQuery({
    queryKey: ['search', 'github', query, page],
    queryFn: () => searchApi.searchGithub({ q: query, page, per_page: 10 }),
    enabled: !!query,
  });

  return {
    results: data?.data,
    isLoading,
    error,
    refetch,
  };
}
```

- [ ] **Step 2: 创建SearchBar组件**

```tsx
'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';

export function SearchBar() {
  const [keyword, setKeyword] = useState('');
  const router = useRouter();

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    if (keyword.trim()) {
      router.push(`/search?q=${encodeURIComponent(keyword.trim())}`);
    }
  };

  return (
    <form onSubmit={handleSearch} className="w-full max-w-2xl">
      <div className="flex gap-2">
        <input
          type="text"
          value={keyword}
          onChange={(e) => setKeyword(e.target.value)}
          placeholder="搜索代码仓库..."
          className="flex-1 px-4 py-3 text-lg border rounded-lg"
        />
        <button type="submit" className="px-6 py-3 bg-blue-600 text-white rounded-lg">
          搜索
        </button>
      </div>
    </form>
  );
}
```

- [ ] **Step 3: 创建SearchResultCard组件**

```tsx
import { GithubSearchItem } from '@/lib/api/types';

interface SearchResultCardProps {
  item: GithubSearchItem;
}

export function SearchResultCard({ item }: SearchResultCardProps) {
  return (
    <a
      href={item.html_url}
      target="_blank"
      rel="noopener noreferrer"
      className="block p-4 border rounded-lg hover:shadow-md transition-shadow"
    >
      <div className="flex justify-between items-start">
        <div>
          <h3 className="text-lg font-semibold text-blue-600">{item.full_name}</h3>
          <p className="mt-1 text-gray-600 line-clamp-2">
            {item.description || '暂无描述'}
          </p>
        </div>
        <div className="flex items-center gap-4 text-sm text-gray-500">
          <span>⭐ {item.stargazers_count.toLocaleString()}</span>
          {item.language && <span>{item.language}</span>}
        </div>
      </div>
    </a>
  );
}
```

- [ ] **Step 4: 创建SearchResultList组件**

```tsx
import { SearchResultCard } from './SearchResultCard';
import { GithubSearchResponse } from '@/lib/api/types';

interface SearchResultListProps {
  results: GithubSearchResponse | undefined;
}

export function SearchResultList({ results }: SearchResultListProps) {
  if (!results) return null;

  if (results.items.length === 0) {
    return <div className="text-center py-8 text-gray-500">未找到相关结果</div>;
  }

  return (
    <div className="space-y-4">
      <div className="text-gray-500">
        找到 {results.total_count.toLocaleString()} 个结果
      </div>
      {results.items.map((item) => (
        <SearchResultCard key={item.id} item={item} />
      ))}
    </div>
  );
}
```

- [ ] **Step 5: 创建搜索结果页面**

```tsx
'use client';

import { useSearch } from '@/modules/search/hooks/useSearch';
import { SearchResultList } from '@/components/search/SearchResultList';
import { SearchBar } from '@/components/search/SearchBar';

export default function SearchPage() {
  const { results, isLoading, error } = useSearch();

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="mb-8">
        <SearchBar />
      </div>

      {isLoading && <div className="text-center py-8">加载中...</div>}
      
      {error && (
        <div className="text-center py-8 text-red-500">
          搜索失败: {error.message}
        </div>
      )}

      {!isLoading && !error && <SearchResultList results={results} />}
    </div>
  );
}
```

- [ ] **Step 6: 创建首页**

```tsx
import { SearchBar } from '@/components/search/SearchBar';

export default function HomePage() {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center px-4">
      <h1 className="text-4xl font-bold mb-8">OneSearch 一搜</h1>
      <p className="text-xl text-gray-600 mb-8">
        开发者一站式信息搜索工具
      </p>
      <SearchBar />
    </div>
  );
}
```

---

## 验证步骤

### 后端验证
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
# 访问 http://localhost:8000/docs 查看API文档
```

### 前端验证
```bash
cd frontend
npm install
npm run dev
# 访问 http://localhost:3000 查看页面
```

### 联调验证
1. 后端启动：`uvicorn app.main:app --reload --port 8000`
2. 前端启动：`npm run dev`
3. 测试注册流程
4. 测试登录流程
5. 测试GitHub搜索功能

---

## 实施顺序

1. **Phase 1** (基础架构) - 可并行
   - Task 1.1: 前端项目初始化
   - Task 1.2: 后端项目初始化
   - Task 1.3: 数据库配置

2. **Phase 2** (核心模块) - Phase 1完成后
   - Task 2.1: 后端Core模块
   - Task 2.2: 前端API客户端

3. **Phase 3** (认证模块) - Phase 2完成后
   - Task 3.1: 后端认证API
   - Task 3.2: 前端认证页面

4. **Phase 4** (搜索模块) - Phase 2完成后
   - Task 4.1: 后端搜索API
   - Task 4.2: 前端搜索页面

---

**计划状态：** 待实施
**最后更新：** 2026-05-08
