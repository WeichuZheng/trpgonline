# TRPG Online - 配置文件
import os
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # 服务器
    host: str = "0.0.0.0"
    port: int = 8000

    # 数据库
    database_url: str = "sqlite+aiosqlite:///./database.db"

    # JWT 认证
    secret_key: str = "dev-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # 文件上传
    upload_dir: str = "./uploads"
    max_file_size: int = 10 * 1024 * 1024  # 10MB

    # 运行环境
    debug: bool = True
    cors_origins: str = ""  # Comma-separated list of allowed origins for production

    class Config:
        env_file = ".env"
        extra = "allow"


@lru_cache()
def get_settings() -> Settings:
    s = Settings()
    # C3 fix: Warn if using default secret key in production
    if s.secret_key == "dev-secret-key-change-in-production" and not s.debug:
        raise ValueError("生产环境必须设置 SECRET_KEY 环境变量，不能使用默认值")
    return s


settings = get_settings()