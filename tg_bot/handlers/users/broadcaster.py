from loguru import logger
from loader import bot
from aiogram.utils import exceptions
from django.conf import settings
import asyncio
from tg_bot.utils.db_cruds import get_broadcast_list, get_watcher, change_count


async def safe_message_send(tg_id, message):
    try:
        await bot.send_message(tg_id, message)
    except exceptions.BotBlocked:
        logger.error(f"Target [ID:{tg_id}]: blocked by user")
    except exceptions.ChatNotFound:
        logger.error(f"Target [ID:{tg_id}]: invalid user ID")
    except exceptions.RetryAfter as e:
        logger.error(
            f"Target [ID:{tg_id}]: Flood limit is exceeded. \
            Sleep {e.timeout} seconds."
        )
        await asyncio.sleep(e.timeout)
        return await safe_message_send(tg_id, message)  # Recursive call
    except exceptions.UserDeactivated:
        logger.error(f"Target [ID:{tg_id}]: user is deactivated")
    except exceptions.TelegramAPIError:
        logger.exception(f"Target [ID:{tg_id}]: failed")
    else:
        logger.info(f"Target [ID:{tg_id}]: success")
        return True
    return False


async def sentinel():
    for admin in settings.ADMINS_LIST:
        try:
            text = 'Бот запущен и готов к работе'
            await bot.send_message(chat_id=admin, text=text)
        except Exception as err:
            logger.exception(err)
    while 1:
        result_watcher = await get_watcher()
        if result_watcher:
            topic, speaker, status = result_watcher
            hearers = await get_broadcast_list()
            message = f' Доклад {topic}, докладчик: {speaker} {status}'
            for hearer in hearers:
                await safe_message_send(
                    hearer,
                    message
                )
            await change_count()
        await asyncio.sleep(3)


async def broadcaster(message):
    count = 0
    broadcast_list = await get_broadcast_list()
    try:
        for tg_id in broadcast_list:
            if await safe_message_send(tg_id, message):
                count += 1
            await asyncio.sleep(.05)  # 20 messages per second (30 лимит)
    finally:
        logger.info(f"{count} messages successful sent.")

    return count
