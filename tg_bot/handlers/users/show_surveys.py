from aiogram import types
from aiogram.dispatcher.filters import Text
from loader import dp

from tg_bot.states.states import UserState, SurveyState
from tg_bot.utils.db_cruds import get_surveys
from tg_bot.messages.messages import get_report_button_caption
@dp.callback_query_handler(Text('reports'), state=[UserState, SurveyState, None])
async def intro(cb: types.CallbackQuery):
    reports = await get_surveys()
    if reports:
        reports_markup = types.InlineKeyboardMarkup(row_width=1)
        reports_btn = []
        for report in reports:
            reports_btn.append(types.InlineKeyboardButton(
                f'Докладчик: {report["speaker"]}, начало: {report["starts_at"]}-конец:{report["ends_at"]}',
                callback_data=f'/{report["id"]}'))
        reports_markup.add(*reports_btn)
        await cb.message.answer(f'Choose report', reply_markup=reports_markup)
        await UserState.report.set()
        await cb.answer()
