"""
Telegram Multi-Bot Configuration
"""

import os
from dataclasses import dataclass

from dotenv import load_dotenv

# Načítanie .env súboru
load_dotenv()


@dataclass
class BotConfig:
    """Konfigurácia pre jednotlivý bot"""

    token: str
    tenant: str | None  # None = admin bot (prepínateľný)
    requires_approval: bool
    name: str


@dataclass
class Settings:
    """Hlavná konfigurácia"""

    # NEX Brain API
    nex_brain_api_url: str = os.getenv("NEX_BRAIN_API_URL", "http://localhost:8001")

    # História konverzácie
    history_max_messages: int = 10
    history_timeout_minutes: int = 30

    # Formátovanie
    show_sources: bool = True
    max_sources_display: int = 3

    # Bot tokeny z .env
    admin_bot_token: str = os.getenv("TELEGRAM_ADMIN_BOT_TOKEN", "")
    icc_bot_token: str = os.getenv("TELEGRAM_ICC_BOT_TOKEN", "")
    andros_bot_token: str = os.getenv("TELEGRAM_ANDROS_BOT_TOKEN", "")

    def get_bots(self) -> dict[str, BotConfig]:
        """Vráti konfiguráciu všetkých botov"""
        bots = {}

        if self.admin_bot_token:
            bots["admin"] = BotConfig(
                token=self.admin_bot_token, tenant=None, requires_approval=False, name="NEX Brain Admin"
            )

        if self.icc_bot_token:
            bots["icc"] = BotConfig(
                token=self.icc_bot_token, tenant="icc", requires_approval=True, name="NEX Brain ICC"
            )

        if self.andros_bot_token:
            bots["andros"] = BotConfig(
                token=self.andros_bot_token, tenant="andros", requires_approval=True, name="NEX Brain ANDROS"
            )

        return bots


settings = Settings()
