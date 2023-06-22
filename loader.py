from aiogram import Bot, Dispatcher, types
from django.conf import settings
from aiogram.contrib.fsm_storage.memory import MemoryStorage


bot = Bot(settings.TELEGRAM_BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)