"""
Setup Telegram Bot pre NEX Brain
Vytvorí štruktúru a základné súbory
"""
from pathlib import Path

BOT_DIR = Path("apps/nex-brain/telegram")

FILES = {
    "__init__.py": '''"""NEX Brain Telegram Bot"""
''',

    "bot.py": '''"""
NEX Brain Telegram Bot
Hlavný modul pre Telegram integráciu
"""
import asyncio
import logging
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)
import httpx
from config import settings

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# NEX Brain API endpoint
API_URL = settings.nex_brain_api_url


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handler pre /start príkaz"""
    user = update.effective_user
    await update.message.reply_text(
        f"Ahoj {user.first_name}! 👋\\n\\n"
        f"Som NEX Brain - inteligentný asistent pre váš NEX systém.\\n\\n"
        f"Môžete sa ma opýtať na:\\n"
        f"• Firemné procesy a postupy\\n"
        f"• Informácie z dokumentácie\\n"
        f"• Stav objednávok a faktúr\\n\\n"
        f"Jednoducho napíšte svoju otázku!"
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handler pre /help príkaz"""
    await update.message.reply_text(
        "🧠 *NEX Brain - Pomocník*\\n\\n"
        "*Príkazy:*\\n"
        "/start - Spustenie bota\\n"
        "/help - Táto správa\\n"
        "/tenant - Zmena tenant (icc/andros)\\n\\n"
        "*Ako používať:*\\n"
        "Jednoducho napíšte svoju otázku v prirodzenom jazyku.\\n\\n"
        "*Príklady:*\\n"
        "• Ako spracujem reklamáciu?\\n"
        "• Aké sú BOZP pravidlá?\\n"
        "• Kto schvaľuje dovolenky?",
        parse_mode="Markdown"
    )


async def set_tenant(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handler pre /tenant príkaz"""
    if not context.args:
        current = context.user_data.get("tenant", "icc")
        await update.message.reply_text(
            f"Aktuálny tenant: *{current}*\\n\\n"
            f"Použitie: /tenant icc alebo /tenant andros",
            parse_mode="Markdown"
        )
        return

    tenant = context.args[0].lower()
    if tenant not in ["icc", "andros"]:
        await update.message.reply_text("❌ Neplatný tenant. Použite: icc alebo andros")
        return

    context.user_data["tenant"] = tenant
    await update.message.reply_text(f"✅ Tenant nastavený na: *{tenant}*", parse_mode="Markdown")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handler pre bežné správy - dotazy na NEX Brain"""
    user_message = update.message.text
    tenant = context.user_data.get("tenant", "icc")

    # Typing indicator
    await update.message.chat.send_action("typing")

    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                f"{API_URL}/chat",
                json={
                    "message": user_message,
                    "tenant": tenant
                }
            )
            response.raise_for_status()
            data = response.json()
            answer = data.get("response", "Prepáčte, nepodarilo sa spracovať dotaz.")

    except httpx.TimeoutException:
        answer = "⏱️ Odpoveď trvá príliš dlho. Skúste to znova."
    except httpx.HTTPError as e:
        logger.error(f"API error: {e}")
        answer = "❌ Chyba pri komunikácii s NEX Brain API."
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        answer = "❌ Nastala neočakávaná chyba."

    await update.message.reply_text(answer)


def main() -> None:
    """Spustenie bota"""
    if not settings.telegram_bot_token:
        raise ValueError("TELEGRAM_BOT_TOKEN nie je nastavený!")

    # Vytvorenie aplikácie
    application = Application.builder().token(settings.telegram_bot_token).build()

    # Handlery
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("tenant", set_tenant))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Spustenie
    logger.info("NEX Brain Telegram Bot starting...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
''',

    "config.py": '''"""
Telegram Bot Configuration
"""
import os
from dataclasses import dataclass


@dataclass
class Settings:
    telegram_bot_token: str = os.getenv("TELEGRAM_BOT_TOKEN", "")
    nex_brain_api_url: str = os.getenv("NEX_BRAIN_API_URL", "http://localhost:8000")


settings = Settings()
''',

    "requirements.txt": '''python-telegram-bot>=20.7
httpx>=0.25.0
''',
}


def main():
    print("=" * 70)
    print("SETUP: NEX Brain Telegram Bot")
    print("=" * 70)

    # Vytvor adresár
    BOT_DIR.mkdir(parents=True, exist_ok=True)
    print(f"✅ Adresár: {BOT_DIR}")

    # Vytvor súbory
    for filename, content in FILES.items():
        filepath = BOT_DIR / filename
        filepath.write_text(content, encoding='utf-8')
        print(f"✅ Vytvorený: {filepath}")

    print("\n" + "=" * 70)
    print("ĎALŠIE KROKY:")
    print("=" * 70)
    print("1. Nainštaluj závislosti:")
    print("   pip install python-telegram-bot httpx")
    print()
    print("2. Nastav environment variables:")
    print("   $env:TELEGRAM_BOT_TOKEN='8585064403:AAFHf_xXeA43QBWUcObjt6pYA3xOFPjVpjg'")
    print("   $env:NEX_BRAIN_API_URL='http://localhost:8000'")
    print()
    print("3. Spusti bot:")
    print("   python apps/nex-brain/telegram/bot.py")
    print("=" * 70)


if __name__ == "__main__":
    main()