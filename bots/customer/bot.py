import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.enums import ParseMode

from config import Config
from .handlers import router


# =====================================
# LOGGING
# =====================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)

logger = logging.getLogger(__name__)


# =====================================
# TOKEN
# =====================================

BOT_TOKEN = (
    getattr(Config, "TG_BOT_TOKEN", None)
    or os.getenv("TG_BOT_TOKEN")
)

if not BOT_TOKEN:
    raise Exception(
        "TG_BOT_TOKEN topilmadi. .env yoki Render Environment ga qo'shing"
    )


# =====================================
# SESSION
# =====================================

session = AiohttpSession(
    timeout=60
)


# =====================================
# BOT
# =====================================

bot = Bot(
    token=BOT_TOKEN,
    session=session,
    default=DefaultBotProperties(
        parse_mode=ParseMode.HTML
    )
)


# =====================================
# DISPATCHER
# =====================================

dp = Dispatcher()

dp.include_router(router)


# =====================================
# STARTUP
# =====================================

async def on_startup():

    await bot.delete_webhook(
        drop_pending_updates=True
    )

    me = await bot.get_me()

    logger.info(
        """
==================================
 Vendora Customer Bot
==================================

BOT ISHGA TUSHDI ✅

Username:
@%s

ID:
%s

==================================
        """,
        me.username,
        me.id
    )


# =====================================
# SHUTDOWN
# =====================================

async def on_shutdown():

    logger.info(
        "Bot to'xtatilmoqda..."
    )

    await bot.session.close()

    logger.info(
        "Session yopildi ✅"
    )


# =====================================
# MAIN BOT LOOP
# =====================================

async def start_bot():

    try:

        await on_startup()

        await dp.start_polling(
            bot,
            allowed_updates=dp.resolve_used_update_types()
        )

    except Exception:

        logger.exception(
            "Bot ishlashida xato"
        )

    finally:

        await on_shutdown()



# =====================================
# FLASK THREAD UCHUN
# =====================================

def run_bot():

    try:
        asyncio.run(
            start_bot()
        )

    except RuntimeError:

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        loop.run_until_complete(
            start_bot()
        )


# =====================================
# DIRECT TEST
# =====================================

if __name__ == "__main__":

    run_bot()