from aiogram import types
from aiogram.dispatcher import FSMContext
from loader import dp

from tg_bot.states.states import UserState
from tg_bot.utils.db_cruds import get_report
from tg_bot.keyboards import inline_kb


@dp.callback_query_handler(
        lambda callback_query: callback_query.data[0] == '/',
        state=UserState.report
)
async def manage_report(callback_query: types.CallbackQuery, state: FSMContext):
    report_id = int(callback_query.data[1:])
    report = await get_report(report_id)
    if report['is_current']:
        await callback_query.message.answer(
            f'Доклад сейчас идёт\nТема: {report["topic"]},\nДокладчик: {report["speaker"]},\n'
            f'Начало: {report["starts_at"]},\nКонец: {report["ends_at"]}',
            reply_markup=inline_kb.base_menu
        )
    else:
        await callback_query.message.answer(
            f'Тема: {report["topic"]},\nДокладчик: {report["speaker"]},\nНачало: {report["starts_at"]},'
            f'\nКонец: {report["ends_at"]}', reply_markup=inline_kb.base_menu)
    await state.finish()
    await callback_query.answer()