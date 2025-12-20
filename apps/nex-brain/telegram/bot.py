"""
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
        f"Ahoj {user.first_name}! 👋\n\n"
        f"Som NEX Brain - inteligentný asistent pre váš NEX systém.\n\n"
        f"Môžete sa ma opýtať na:\n"
        f"• Firemné procesy a postupy\n"
        f"• Informácie z dokumentácie\n"
        f"• Stav objednávok a faktúr\n\n"
        f"Jednoducho napíšte svoju otázku!"
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handler pre /help príkaz"""
    await update.message.reply_text(
        "🧠 *NEX Brain - Pomocník*\n\n"
        "*Príkazy:*\n"
        "/start - Spustenie bota\n"
        "/help - Táto správa\n"
        "/tenant - Zmena tenant (icc/andros)\n\n"
        "*Ako používať:*\n"
        "Jednoducho napíšte svoju otázku v prirodzenom jazyku.\n\n"
        "*Príklady:*\n"
        "• Ako spracujem reklamáciu?\n"
        "• Aké sú BOZP pravidlá?\n"
        "• Kto schvaľuje dovolenky?",
        parse_mode="Markdown"
    )


async def set_tenant(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handler pre /tenant príkaz"""
    if not context.args:
        current = context.user_data.get("tenant", "icc")
        await update.message.reply_text(
            f"Aktuálny tenant: *{current}*\n\n"
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
                f"{API_URL}/api/v1/chat",
                json={
                    "question": user_message,
                    "tenant": tenant
                }
            )
            response.raise_for_status()
            data = response.json()
            answer = data.get("answer", "Prepáčte, nepodarilo sa spracovať dotaz.")

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
