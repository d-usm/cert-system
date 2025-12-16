from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "Cert System"
    DATABASE_URL: str = Field("sqlite:///./cert.db", env="DATABASE_URL")
    JWT_SECRET_KEY: str = Field("change-me", env="JWT_SECRET_KEY")
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24
    PUBLIC_BASE_URL: str = Field("http://localhost:8000", env="PUBLIC_BASE_URL")
    CERTIFICATES_DIR: str = Field("certificates", env="CERTIFICATES_DIR")
    ADMIN_EMAIL: str | None = Field(None, env="ADMIN_EMAIL")
    ADMIN_PASSWORD: str | None = Field(None, env="ADMIN_PASSWORD")
    ADMIN_FULLNAME: str = Field("Администратор", env="ADMIN_FULLNAME")

    model_config = SettingsConfigDict(
        env_file=Path(__file__).resolve().parent.parent / ".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )


settings = Settings()

