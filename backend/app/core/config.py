from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List


class Settings(BaseSettings):
    PROJECT_NAME: str = "OneSearch"
    VERSION: str = "1.0.0"
    
    DATABASE_URL: str = "postgresql+asyncpg://user:password@localhost:5432/onesearch"
    
    JWT_SECRET_KEY: str = "your-secret-key-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_MINUTES: int = 10080
    
    CORS_ORIGINS: str = "http://localhost:3000"
    
    GITHUB_API_TOKEN: str = ""
    # Gitee OpenAPI v5 私人令牌，用于搜索仓库；不配置时仍尝试匿名（可能被限流或返回空）
    GITEE_ACCESS_TOKEN: str = ""
    
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True, env_nested_delimiter="__")
    
    @property
    def cors_origins_list(self) -> List[str]:
        if not self.CORS_ORIGINS:
            return []
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]


settings = Settings()
