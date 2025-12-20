"""
Telegram Bot Configuration
"""
import os
from dataclasses import dataclass


@dataclass
class Settings:
    telegram_bot_token: str = os.getenv("TELEGRAM_BOT_TOKEN", "")
    nex_brain_api_url: str = os.getenv("NEX_BRAIN_API_URL", "http://localhost:8000")


settings = Settings()
