from aiogram import types
from aiogram.dispatcher.filters import Text
from loader import dp

from tg_bot.states.states import UserState, SurveyState
from tg_bot.keyboards import inline_kb
from tg_bot.messages.messages import ABOUT_MSG
from tg_bot.utils.db_cruds import is_user_reporter


# @dp.message_handler(commands='start')
# async def command_start(message: types.Message):
#     await message.answer(message.text)


@dp.callback_query_handler(Text('intro'), state=[UserState, SurveyState, None])
async def intro(callback_query: types.CallbackQuery):
    await callback_query.message.answer(
        ABOUT_MSG, reply_markup=inline_kb.hearer_main_menu
    )
    await callback_query.answer()


@dp.message_handler(state=[not SurveyState, UserState, None])
async def start_conversation(message: types.Message):
    reporter = await is_user_reporter(message.from_user.id)
    if not reporter:
        await message.answer(
            f'Здравствуйте ГОСТЬ: {message.from_user.username} для выхода в любом месте наберите "exit", '
            f'для подробного ознакомления с функциональностью чата нажмите кнопку "О нас"',
            reply_markup=inline_kb.base_menu
        )
        await message.answer(
            'Сделайте выбор',
            reply_markup=inline_kb.hearer_main_menu
        )
    else:
        await message.answer(
            f'Здравствуйте  ДОКЛАДЧИК: {message.from_user.username} для выхода в любом месте наберите "exit",',
            reply_markup=inline_kb.base_menu
        )
        await message.answer(
            'Сделайте выбор',
            reply_markup=inline_kb.reporter_main_menu
        )
