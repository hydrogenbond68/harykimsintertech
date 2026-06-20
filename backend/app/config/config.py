from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    DATABASE_URL: str
    JWT_SECRET_KEY: str
    JWT_REFRESH_SECRET: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    DODO_API_KEY: Optional[str] = None
    DODO_SECRET_KEY: Optional[str] = None
    DODO_WEBHOOK_SECRET: Optional[str] = None
    DODO_ENVIRONMENT: str = "test_mode"
    
    CLOUDINARY_URL: Optional[str] = None
    
    SMTP_HOST: Optional[str] = None
    SMTP_PORT: Optional[int] = 587
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    
    FRONTEND_URL: str = "http://localhost:5173"
    BACKEND_URL: str = "http://localhost:8000"
    
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
