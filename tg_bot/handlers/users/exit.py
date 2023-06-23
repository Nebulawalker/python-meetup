from aiogram import types
from aiogram.dispatcher import FSMContext
from loader import dp
from tg_bot.keyboards import inline_kb

from tg_bot.states.states import UserState, SurveyState


@dp.message_handler(text='exit', state=[UserState, SurveyState, None, '*'])
async def exit_proceed(msg: types.Message, state: FSMContext):
    await msg.answer('Всего доброго, берегите себя', reply_markup=inline_kb.base_menu)
    await state.finish()
