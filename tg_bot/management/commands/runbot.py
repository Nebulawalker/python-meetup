from django.core.management.base import BaseCommand

from aiogram import executor

from loader import dp

import asyncio

from tg_bot.handlers.users.broadcaster import sentinel

from loguru import logger

logger.add(
    'log/debug.log',
    format='{time}  {level}  {message}',
    level='DEBUG',
    rotation='1 week'
)


async def on_startup(dispatcher):
    asyncio.create_task(sentinel())
    logger.info('Бот запущен')


class Command(BaseCommand):
    help = 'RUN COMMAND: python manage.py runbot'

    def handle(self, *args, **options):
        executor.start_polling(
            dp,
            skip_updates=True,
            on_startup=on_startup
        )
