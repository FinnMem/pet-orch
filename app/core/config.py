from pydantic import BaseSettings, Field
from typing import Optional
import os
from vault import load_vault_secrets

class Settings(BaseSettings):
    database_url: str = Field(..., alias="DATABASE_URL")
    redis_url: str = Field(..., alias="REDIS_URL")
    telegram_token: Optional[str] = Field(None, alias="TELEGRAM_TOKEN")
    telegram_chat_id: Optional[str] = Field(None, alias="TELEGRAM_CHAT_ID")

    class Config:
        env_file = ".env"
        extra = "ignore"

# Пробуем загрузить из Vault, если нет — fallback на .env
try:
    vault_data = load_vault_secrets()
    settings = Settings(**vault_data)
except Exception:
    settings = Settings()
