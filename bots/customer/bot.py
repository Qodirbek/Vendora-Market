import asyncio
import logging

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
    format=(
        "%(asctime)s | "
        "%(levelname)s | "
        "%(name)s | "
        "%(message)s"
    )
)


logger = logging.getLogger(__name__)




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

    token=Config.TG_BOT_TOKEN,

    session=session,

    default=DefaultBotProperties(

        parse_mode=ParseMode.HTML

    )

)




# =====================================
# DISPATCHER
# =====================================

dp = Dispatcher()


dp.include_router(
    router
)




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
 Telegram Auth System
==================================

Bot ishga tushdi ✅

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


    await session.close()


    logger.info(
        "Session yopildi ✅"
    )





# =====================================
# MAIN
# =====================================

async def main():


    try:

        await on_startup()


        await dp.start_polling(

            bot,

            allowed_updates=
            dp.resolve_used_update_types()

        )


    except Exception as e:


        logger.exception(

            f"Bot xatosi: {e}"

        )


    finally:


        await on_shutdown()




# =====================================
# RUN
# =====================================

if __name__ == "__main__":

    asyncio.run(
        main()
    )