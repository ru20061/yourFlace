import os
import json
from pathlib import Path
from dotenv import load_dotenv

# .env 파일 로드
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(env_path)


def _get(key: str, default: str = "") -> str:
    return os.getenv(key, default)


def _get_int(key: str, default: int = 0) -> int:
    return int(os.getenv(key, str(default)))


def _get_bool(key: str, default: bool = False) -> bool:
    return os.getenv(key, str(default)).lower() in ("true", "1", "yes")


def _get_list(key: str, default: list | None = None) -> list:
    raw = os.getenv(key)
    if raw:
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            return raw.split(",")
    return default or []


class Settings:
    # App
    APP_NAME: str = _get("APP_NAME", "Fanbase Platform")
    APP_VERSION: str = _get("APP_VERSION", "1.0.0")
    DEBUG: bool = _get_bool("DEBUG", True)

    # Database
    DATABASE_HOST: str = _get("DATABASE_HOST", "localhost")
    DATABASE_PORT: int = _get_int("DATABASE_PORT", 5432)
    DATABASE_NAME: str = _get("DATABASE_NAME", "yourflace")
    DATABASE_USERNAME: str = _get("DATABASE_USERNAME", "postgres")
    DATABASE_PASSWORD: str = _get("DATABASE_PASSWORD", "")
    DB_POOL_SIZE: int = _get_int("DB_POOL_SIZE", 20)
    DB_MAX_OVERFLOW: int = _get_int("DB_MAX_OVERFLOW", 40)

    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql://{self.DATABASE_USERNAME}:{self.DATABASE_PASSWORD}@{self.DATABASE_HOST}:{self.DATABASE_PORT}/{self.DATABASE_NAME}"

    # Redis
    REDIS_URL: str = _get("REDIS_URL", "redis://localhost:6379/0")
    REDIS_MAX_CONNECTIONS: int = _get_int("REDIS_MAX_CONNECTIONS", 50)

    # Elasticsearch
    ELASTICSEARCH_URL: str = _get("ELASTICSEARCH_URL", "http://localhost:9200")
    ELASTICSEARCH_INDEX_PREFIX: str = _get("ELASTICSEARCH_INDEX_PREFIX", "fanbase")

    # Cloudflare R2
    CLOUDFLARE_R2_ACCESS_KEY: str = _get("CLOUDFLARE_R2_ACCESS_KEY", "dev")
    CLOUDFLARE_R2_SECRET_KEY: str = _get("CLOUDFLARE_R2_SECRET_KEY", "dev")
    CLOUDFLARE_R2_BUCKET: str = _get("CLOUDFLARE_R2_BUCKET", "dev")
    CLOUDFLARE_R2_ENDPOINT: str = _get("CLOUDFLARE_R2_ENDPOINT", "http://localhost:9000")
    CLOUDFLARE_R2_PUBLIC_URL: str = _get("CLOUDFLARE_R2_PUBLIC_URL", "http://localhost:9000/dev")

    # JWT
    JWT_SECRET: str = _get("JWT_SECRET", "dev-secret-key-change-in-production")
    JWT_ALGORITHM: str = _get("JWT_ALGORITHM", "HS256")
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = _get_int("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", 30)
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = _get_int("JWT_REFRESH_TOKEN_EXPIRE_DAYS", 7)

    # OAuth
    OAUTH_GOOGLE_CLIENT_ID: str = _get("OAUTH_GOOGLE_CLIENT_ID", "dev")
    OAUTH_GOOGLE_CLIENT_SECRET: str = _get("OAUTH_GOOGLE_CLIENT_SECRET", "dev")
    OAUTH_KAKAO_CLIENT_ID: str = _get("OAUTH_KAKAO_CLIENT_ID", "dev")
    OAUTH_KAKAO_CLIENT_SECRET: str = _get("OAUTH_KAKAO_CLIENT_SECRET", "dev")
    OAUTH_NAVER_CLIENT_ID: str = _get("OAUTH_NAVER_CLIENT_ID", "")
    OAUTH_NAVER_CLIENT_SECRET: str = _get("OAUTH_NAVER_CLIENT_SECRET", "")

    # CORS
    CORS_ORIGINS: list = _get_list("CORS_ORIGINS", ["http://localhost:3000", "http://localhost"])

    # File Upload
    MAX_UPLOAD_SIZE: int = _get_int("MAX_UPLOAD_SIZE", 100 * 1024 * 1024)
    ALLOWED_IMAGE_TYPES: list = _get_list("ALLOWED_IMAGE_TYPES", ["image/jpeg", "image/png", "image/webp", "image/gif"])
    ALLOWED_VIDEO_TYPES: list = _get_list("ALLOWED_VIDEO_TYPES", ["video/mp4", "video/webm"])


settings = Settings()
