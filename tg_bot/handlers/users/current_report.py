from aiogram import types
from aiogram.dispatcher import FSMContext
from loader import dp

from tg_bot.states.states import UserState, MessageState
from tg_bot.utils.db_cruds import get_report
from tg_bot.keyboards import inline_kb
from tg_bot.messages.messages import get_report_description


@dp.callback_query_handler(
        lambda callback_query: callback_query.data[0] == '/',
        state=UserState.report
)
async def manage_report(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.edit_reply_markup()
    report_id = int(callback_query.data[1:])
    report = await get_report(report_id)
    await callback_query.message.answer(
            await get_report_description(report))
    await state.finish()
    if report['is_current']:

        await state.update_data(report_id=report['id'])
        await callback_query.message.answer('Прямо сейчас идет доклад, Вы можете задать вопрос спикеру!',
                                            reply_markup=inline_kb.question_menu)

    await callback_query.answer()
