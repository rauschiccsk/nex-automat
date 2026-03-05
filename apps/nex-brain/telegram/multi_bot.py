"""
NEX Brain Multi-Bot System
Spúšťa Admin, ICC a ANDROS boty v jednom procese
"""

import asyncio
import logging
import time
from datetime import datetime, timedelta
from typing import Any

import httpx
from nex_config.timeouts import TELEGRAM_LLM_TIMEOUT_SECONDS
from user_manager import UserManager

from config import BotConfig, settings
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

# Logging
try:
    from db import log_query, update_feedback

    DB_AVAILABLE = True
except ImportError:
    DB_AVAILABLE = False
    log_query = None
    update_feedback = None

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# NEX Brain API endpoint
API_URL = settings.nex_brain_api_url

# In-memory história konverzácií
conversation_history: dict[int, dict[str, Any]] = {}

# Mapovanie message_id -> log_id pre feedback
message_log_map: dict[int, int] = {}

# Reference na admin bota pre notifikácie
admin_bot: Bot | None = None
ADMIN_USER_ID: int = 7204918893  # Tvoje user_id pre notifikácie


def get_user_history(user_id: int) -> dict[str, Any]:
    """Získanie alebo vytvorenie histórie pre používateľa"""
    now = datetime.now()

    if user_id in conversation_history:
        history = conversation_history[user_id]
        timeout = timedelta(minutes=settings.history_timeout_minutes)
        if now - history["last_activity"] > timeout:
            history = {
                "messages": [],
                "last_activity": now,
                "tenant": history.get("tenant", "icc"),
            }
            conversation_history[user_id] = history
        else:
            history["last_activity"] = now
    else:
        history = {"messages": [], "last_activity": now, "tenant": "icc"}
        conversation_history[user_id] = history

    return history


def add_to_history(user_id: int, role: str, content: str) -> None:
    """Pridanie správy do histórie"""
    history = get_user_history(user_id)
    history["messages"].append({"role": role, "content": content})

    max_messages = settings.history_max_messages
    if len(history["messages"]) > max_messages:
        history["messages"] = history["messages"][-max_messages:]


def format_response(answer: str, sources: list = None) -> str:
    """Formátovanie odpovede"""
    formatted = f"📋 *Odpoveď:*\n\n{answer}"

    if sources and settings.show_sources:
        sources_display = sources[: settings.max_sources_display]
        formatted += "\n\n📚 *Zdroje:*\n"
        for source in sources_display:
            if isinstance(source, dict):
                filename = source.get("filename", str(source))
            else:
                filename = str(source)
            short_name = filename.split("/")[-1] if "/" in filename else filename
            formatted += f"• `{short_name}`\n"

    return formatted


def get_feedback_keyboard() -> InlineKeyboardMarkup:
    """Inline klávesnica pre feedback"""
    keyboard = [
        [
            InlineKeyboardButton("👍 Užitočné", callback_data="feedback_good"),
            InlineKeyboardButton("👎 Neužitočné", callback_data="feedback_bad"),
        ]
    ]
    return InlineKeyboardMarkup(keyboard)


def create_bot_handlers(bot_config: BotConfig, bot_key: str):
    """Vytvorenie handlerov pre konkrétny bot"""

    async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handler pre /start"""
        user = update.effective_user
        user_id = user.id
        username = user.username or ""
        first_name = user.first_name or ""

        # Admin bot - bez schvaľovania
        if not bot_config.requires_approval:
            get_user_history(user_id)
            await update.message.reply_text(
                f"Ahoj {first_name}! 👋\n\n"
                f"Som *{bot_config.name}* - admin rozhranie.\n\n"
                f"*Admin príkazy:*\n"
                f"/pending - čakajúci používatelia\n"
                f"/approve `user_id` `tenant` - schválenie\n"
                f"/reject `user_id` `tenant` - zamietnutie\n"
                f"/users - schválení používatelia\n"
                f"/tenant - zmena tenant\n\n"
                f"Alebo napíš otázku pre NEX Brain.",
                parse_mode="Markdown",
            )
            return

        # Tenant boty - vyžadujú schválenie
        tenant = bot_config.tenant

        # Kontrola či je schválený
        if UserManager.is_approved(user_id, tenant):
            await update.message.reply_text(
                f"Vitajte späť, {first_name}! 👋\n\nSom *{bot_config.name}*.\nNapíšte svoju otázku.",
                parse_mode="Markdown",
            )
            return

        # Kontrola či už čaká
        if UserManager.is_pending(user_id, tenant):
            await update.message.reply_text(
                f"⏳ *Čakáte na schválenie*\n\n"
                f"Váša žiadosť o prístup do {bot_config.name} "
                f"bola odoslaná a čaká na schválenie administrátorom.",
                parse_mode="Markdown",
            )
            return

        # Nová žiadosť
        UserManager.request_access(user_id, username, first_name, tenant)

        await update.message.reply_text(
            f"👋 Vitajte v *{bot_config.name}*!\n\n"
            f"⏳ Vaša žiadosť o prístup bola odoslaná.\n"
            f"Administrátor vás čoskoro schváli.\n\n"
            f"Dostanete správu keď budete schválený.",
            parse_mode="Markdown",
        )

        # Notifikácia adminovi
        if admin_bot:
            try:
                await admin_bot.send_message(
                    chat_id=ADMIN_USER_ID,
                    text=f"🆕 *Nová žiadosť o prístup*\n\n"
                    f"👤 Meno: {first_name}\n"
                    f"📛 Username: @{username}\n"
                    f"🆔 User ID: `{user_id}`\n"
                    f"🏢 Tenant: *{tenant}*\n\n"
                    f"Pre schválenie: `/approve {user_id} {tenant}`\n"
                    f"Pre zamietnutie: `/reject {user_id} {tenant}`",
                    parse_mode="Markdown",
                )
            except Exception as e:
                logger.error(f"Failed to send admin notification: {e}")

    async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handler pre /help"""
        await update.message.reply_text(
            f"🧠 *{bot_config.name} - Pomocník*\n\n"
            f"Jednoducho napíšte svoju otázku.\n\n"
            f"*Príklady:*\n"
            f"• Ako spracujem reklamáciu?\n"
            f"• Aké sú BOZP pravidlá?\n"
            f"• Kto schvaľuje dovolenky?",
            parse_mode="Markdown",
        )

    async def handle_message(
        update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        """Handler pre správy"""
        user = update.effective_user
        user_id = user.id
        user_message = update.message.text
        username = user.username or user.first_name

        # Určenie tenantu
        if bot_config.tenant:
            tenant = bot_config.tenant
            # Kontrola schválenia
            if bot_config.requires_approval and not UserManager.is_approved(
                user_id, tenant
            ):
                if UserManager.is_pending(user_id, tenant):
                    await update.message.reply_text(
                        "⏳ Stále čakáte na schválenie.", parse_mode="Markdown"
                    )
                else:
                    await update.message.reply_text(
                        "❌ Nemáte prístup. Použite /start pre žiadosť.",
                        parse_mode="Markdown",
                    )
                return
        else:
            # Admin bot - použiť tenant z histórie
            history = get_user_history(user_id)
            tenant = history.get("tenant", "icc")

        add_to_history(user_id, "user", user_message)
        await update.message.chat.send_action("typing")

        start_time = time.time()
        sources_str = None
        log_id = None

        try:
            history = get_user_history(user_id)
            context_messages = history["messages"][:-1]

            async with httpx.AsyncClient(
                timeout=TELEGRAM_LLM_TIMEOUT_SECONDS
            ) as client:
                response = await client.post(
                    f"{API_URL}/api/v1/chat",
                    json={
                        "question": user_message,
                        "tenant": tenant,
                        "history": context_messages,
                    },
                )
                response.raise_for_status()
                data = response.json()

                answer = data.get("answer", "Prepáčte, nepodarilo sa spracovať dotaz.")
                sources = data.get("sources", [])

                if sources:
                    source_names = []
                    for s in sources[:3]:
                        if isinstance(s, dict):
                            source_names.append(s.get("filename", "unknown"))
                        else:
                            source_names.append(str(s))
                    sources_str = ", ".join(source_names)

                add_to_history(user_id, "assistant", answer)
                formatted = format_response(answer, sources)
                show_feedback = True

        except httpx.TimeoutException:
            answer = "Timeout"
            formatted = "⏱️ *Timeout*\n\nSkúste to znova."
            show_feedback = False
        except Exception as e:
            logger.error(f"Error: {e}")
            answer = str(e)
            formatted = "❌ *Chyba*\n\nNastala chyba."
            show_feedback = False

        response_time_ms = int((time.time() - start_time) * 1000)

        if DB_AVAILABLE and log_query:
            try:
                log_id = log_query(
                    user_id=user_id,
                    username=username,
                    tenant=tenant,
                    question=user_message,
                    answer=answer[:1000] if answer else None,
                    sources=sources_str,
                    response_time_ms=response_time_ms,
                )
            except Exception as e:
                logger.warning(f"Log failed: {e}")

        if show_feedback:
            sent = await update.message.reply_text(
                formatted, parse_mode="Markdown", reply_markup=get_feedback_keyboard()
            )
            if log_id:
                message_log_map[sent.message_id] = log_id
        else:
            await update.message.reply_text(formatted, parse_mode="Markdown")

    async def handle_feedback(
        update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        """Handler pre feedback"""
        query = update.callback_query
        await query.answer()

        message_id = query.message.message_id
        log_id = message_log_map.get(message_id)

        feedback = "good" if query.data == "feedback_good" else "bad"
        response_text = (
            "👍 Ďakujeme!" if feedback == "good" else "👎 Ďakujeme za feedback."
        )

        if DB_AVAILABLE and update_feedback and log_id:
            try:
                update_feedback(log_id, feedback)
            except:
                pass

        await query.edit_message_text(
            text=f"{query.message.text}\n\n_{response_text}_", parse_mode="Markdown"
        )

    return {
        "start": start,
        "help": help_command,
        "message": handle_message,
        "feedback": handle_feedback,
    }


def create_admin_handlers():
    """Admin-only handlery"""

    async def pending(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Zoznam čakajúcich"""
        users = UserManager.get_pending_users()

        if not users:
            await update.message.reply_text("✅ Žiadni čakajúci používatelia.")
            return

        text = "⏳ *Čakajúci používatelia:*\n\n"
        for u in users:
            text += f"• {u['first_name']} (@{u['username']})\n"
            text += f"  ID: `{u['user_id']}` | Tenant: *{u['tenant']}*\n"
            text += f"  `/approve {u['user_id']} {u['tenant']}`\n\n"

        await update.message.reply_text(text, parse_mode="Markdown")

    async def approve(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Schválenie používateľa"""
        if len(context.args) < 2:
            await update.message.reply_text(
                "Použitie: /approve `user_id` `tenant`", parse_mode="Markdown"
            )
            return

        try:
            user_id = int(context.args[0])
            tenant = context.args[1].lower()
        except:
            await update.message.reply_text("❌ Neplatné parametre")
            return

        admin_id = update.effective_user.id

        if UserManager.approve_user(user_id, tenant, admin_id):
            await update.message.reply_text(
                f"✅ Používateľ `{user_id}` schválený pre *{tenant}*",
                parse_mode="Markdown",
            )

            # Notifikácia používateľovi
            bots = settings.get_bots()
            bot_config = bots.get(tenant)
            if bot_config:
                try:
                    bot = Bot(token=bot_config.token)
                    await bot.send_message(
                        chat_id=user_id,
                        text=f"🎉 *Boli ste schválení!*\n\n"
                        f"Teraz môžete používať {bot_config.name}.\n"
                        f"Napíšte svoju otázku.",
                        parse_mode="Markdown",
                    )
                except Exception as e:
                    logger.error(f"Failed to notify user: {e}")
        else:
            await update.message.reply_text("❌ Chyba pri schvaľovaní")

    async def reject(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Zamietnutie používateľa"""
        if len(context.args) < 2:
            await update.message.reply_text(
                "Použitie: /reject `user_id` `tenant`", parse_mode="Markdown"
            )
            return

        try:
            user_id = int(context.args[0])
            tenant = context.args[1].lower()
        except:
            await update.message.reply_text("❌ Neplatné parametre")
            return

        if UserManager.reject_user(user_id, tenant):
            await update.message.reply_text(
                f"❌ Používateľ `{user_id}` zamietnutý pre *{tenant}*",
                parse_mode="Markdown",
            )
        else:
            await update.message.reply_text("❌ Chyba pri zamietnutí")

    async def users(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Zoznam schválených"""
        approved = UserManager.get_approved_users()

        if not approved:
            await update.message.reply_text("📋 Žiadni schválení používatelia.")
            return

        text = "✅ *Schválení používatelia:*\n\n"
        for u in approved:
            text += f"• {u['first_name']} (@{u['username']})\n"
            text += f"  ID: `{u['user_id']}` | Tenant: *{u['tenant']}*\n\n"

        await update.message.reply_text(text, parse_mode="Markdown")

    async def set_tenant(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Zmena tenant pre admin bota"""
        user_id = update.effective_user.id
        history = get_user_history(user_id)

        if not context.args:
            current = history.get("tenant", "icc")
            await update.message.reply_text(
                f"🏢 Aktuálny tenant: `{current}`\n\nPoužitie: /tenant icc alebo /tenant andros",
                parse_mode="Markdown",
            )
            return

        tenant = context.args[0].lower()
        if tenant not in ["icc", "andros"]:
            await update.message.reply_text("❌ Neplatný tenant.")
            return

        history["tenant"] = tenant
        await update.message.reply_text(f"✅ Tenant: `{tenant}`", parse_mode="Markdown")

    async def status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Status admin bota"""
        user_id = update.effective_user.id
        history = get_user_history(user_id)

        current_tenant = history.get("tenant", "icc")
        message_count = len(history.get("messages", []))

        timeout_mins = settings.history_timeout_minutes
        logging_status = "✅" if DB_AVAILABLE else "❌"

        text = (
            f"📊 **Stav konverzácie**\n\n"
            f"🏢 Tenant: `{current_tenant}`\n"
            f"💬 Správ v histórii: {message_count}/10\n"
            f"⏰ Timeout: {timeout_mins} min\n"
            f"📝 Logging: {logging_status}\n"
        )

        await update.message.reply_text(text, parse_mode="Markdown")

    return {
        "pending": pending,
        "approve": approve,
        "reject": reject,
        "users": users,
        "tenant": set_tenant,
        "status": status,
    }


async def main():
    """Spustenie všetkých botov"""
    global admin_bot

    bots = settings.get_bots()

    if not bots:
        raise ValueError("Žiadne bot tokeny nie sú nastavené!")

    applications = []

    for bot_key, bot_config in bots.items():
        logger.info(f"Inicializujem {bot_config.name}...")

        app = Application.builder().token(bot_config.token).build()
        handlers = create_bot_handlers(bot_config, bot_key)

        app.add_handler(CommandHandler("start", handlers["start"]))
        app.add_handler(CommandHandler("help", handlers["help"]))
        app.add_handler(
            CallbackQueryHandler(handlers["feedback"], pattern="^feedback_")
        )
        app.add_handler(
            MessageHandler(filters.TEXT & ~filters.COMMAND, handlers["message"])
        )

        # Admin handlery len pre admin bota
        if bot_key == "admin":
            admin_handlers = create_admin_handlers()
            app.add_handler(CommandHandler("pending", admin_handlers["pending"]))
            app.add_handler(CommandHandler("approve", admin_handlers["approve"]))
            app.add_handler(CommandHandler("reject", admin_handlers["reject"]))
            app.add_handler(CommandHandler("users", admin_handlers["users"]))
            app.add_handler(CommandHandler("tenant", admin_handlers["tenant"]))
            app.add_handler(CommandHandler("status", admin_handlers["status"]))
            admin_bot = app.bot

        applications.append(app)
        logger.info(f"✅ {bot_config.name} pripravený")

    logger.info(f"Spúšťam {len(applications)} botov...")

    # Inicializácia a spustenie
    for app in applications:
        await app.initialize()
        await app.start()
        await app.updater.start_polling()

    logger.info("🚀 Všetky boty bežia!")

    # Bežať dokým nie je CTRL+C
    try:
        while True:
            await asyncio.sleep(1)
    except asyncio.CancelledError:
        pass
    finally:
        for app in applications:
            await app.updater.stop()
            await app.stop()
            await app.shutdown()


if __name__ == "__main__":
    asyncio.run(main())
