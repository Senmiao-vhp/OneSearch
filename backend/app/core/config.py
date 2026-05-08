from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    PROJECT_NAME: str = "OneSearch"
    VERSION: str = "1.0.0"
    
    DATABASE_URL: str = "postgresql+asyncpg://user:password@localhost:5432/onesearch"
    
    JWT_SECRET_KEY: str = "your-secret-key-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_MINUTES: int = 10080
    
    CORS_ORIGINS: List[str] = ["http://localhost:3000"]
    
    GITHUB_API_TOKEN: str = ""
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
