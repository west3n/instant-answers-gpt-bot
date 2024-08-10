import asyncio
import contextlib
import logging
import sys

from aiogram import Dispatcher

from src.utils import enums, settings
from src.database.models import init_database


async def bot_main():
    logging.basicConfig(level=logging.DEBUG, format="[%(asctime)s] - %(message)s")
    dp = Dispatcher()
    bot = enums.BOT

    try:
        await settings.handlers_registration(dp)
        await settings.middlewares_registration(dp)
        await settings.commands_registration()
        await init_database()
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    except Exception as ex:
        logging.error(f"[Exception] - {ex}", exc_info=True)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    with contextlib.suppress(KeyboardInterrupt, SystemExit):
        asyncio.run(bot_main())
