from loguru import logger

from aiogram import Dispatcher

from django.conf import settings


async def on_startup_notify(dp: Dispatcher):
    for admin in settings.ADMINS_LIST:
        try:
            text = 'Бот запущен и готов к работе'
            await dp.bot.send_message(chat_id=admin, text=text)
        except Exception as err:
            logger.exception(err)
