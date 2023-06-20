from django.core.management.base import BaseCommand

from aiogram import executor

from loader import dp

from tg_bot.handlers import *

from tg_bot.utils.notify_admins import on_startup_notify
from tg_bot.utils.set_bot_commands import set_default_commands

from loguru import logger

logger.add(
    'log/debug.log',
    format='{time}  {level}  {message}',
    level='DEBUG',
    rotation='1 week'
)

async def on_startup(dispatcher):
    await set_default_commands(dispatcher)
    await on_startup_notify(dispatcher)
    logger.info('Бот запущен')


class Command(BaseCommand):
    help = 'RUN COMMAND: python manage.py runbot'

    def handle(self, *args, **options):
        executor.start_polling(
            dp,
            skip_updates=True,
            on_startup=on_startup
        )
