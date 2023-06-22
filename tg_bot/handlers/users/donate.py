from aiogram import types
from aiogram.dispatcher.filters import Text
from loader import dp


@dp.message_handler(commands='donate')
async def donate(message:types.Message):
    await message.answer('Тут будет механизм доната')