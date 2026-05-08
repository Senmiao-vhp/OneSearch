from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.http_client import close_upstream_client
from app.modules.auth.api.endpoints import router as auth_router
from app.modules.search.api.endpoints import router as search_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await close_upstream_client()


def create_app() -> FastAPI:
    app = FastAPI(
        title="OneSearch API",
        description="开发者一站式信息搜索工具 API",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
        lifespan=lifespan,
    )
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    app.include_router(auth_router, prefix="/api/v1")
    app.include_router(search_router, prefix="/api/v1")
    
    return app


app = create_app()


@app.get("/")
async def root():
    return {"message": "OneSearch API", "version": "1.0.0"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
