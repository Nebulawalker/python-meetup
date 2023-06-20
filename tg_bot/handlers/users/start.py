from aiogram import types
from loader import dp


@dp.message_handler(commands='start')
async def command_start(message: types.Message):
    await message.answer(message.text)
        