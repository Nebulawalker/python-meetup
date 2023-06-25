from aiogram import types
from aiogram.dispatcher.filters import Text
from loader import dp

from tg_bot.states.states import UserState, SurveyState
from tg_bot.utils.db_cruds import get_reports
from tg_bot.messages.messages import get_report_button_caption


@dp.callback_query_handler(
        Text('reports'), state=[UserState, SurveyState, None]
)
async def button_show_reports(callback_query: types.CallbackQuery):
    await callback_query.message.edit_reply_markup()
    reports = await get_reports()
    if reports:
        reports_markup = types.InlineKeyboardMarkup(row_width=1)
        reports_btn = []
        for report in reports:
            reports_btn.append(types.InlineKeyboardButton(
                await get_report_button_caption(report),
                callback_data=f'/{report["id"]}'))
        reports_markup.add(*reports_btn)
        await callback_query.message.answer(
            'Нажмите на доклад для подробностей',
            reply_markup=reports_markup
        )
        await UserState.report.set()
    else:
        await callback_query.message.answer(
            'На данный момент докладов нет'
        )
    await callback_query.answer()


@dp.message_handler(commands='reports', state=[UserState, SurveyState, None])
async def show_reports(message: types.Message):
    reports = await get_reports()
    if reports:
        reports_markup = types.InlineKeyboardMarkup(row_width=1)
        reports_btn = []
        for report in reports:
            reports_btn.append(types.InlineKeyboardButton(
                await get_report_button_caption(report),
                callback_data=f'/{report["id"]}'))
        reports_markup.add(*reports_btn)
        await message.answer(
            'Нажмите на доклад для подробностей',
            reply_markup=reports_markup
        )
        await UserState.report.set()
    else:
        await message.answer(
            'На данный момент докладов нет'
        )
