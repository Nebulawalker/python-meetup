from loguru import logger
from aiogram import types
from loader import dp
from loader import bot
from aiogram.utils import exceptions
import asyncio

from tg_bot.utils.db_cruds import get_broadcast_list


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


@dp.message_handler(commands='broadcast')
async def command_broadcast(message: types.Message):
    await broadcaster('test broadcast')
