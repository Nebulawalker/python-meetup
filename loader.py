from aiogram import Bot, Dispatcher, types
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "python_meetup.settings")
django.setup()
from django.conf import settings
from aiogram.contrib.fsm_storage.memory import MemoryStorage


bot = Bot(settings.TELEGRAM_BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
