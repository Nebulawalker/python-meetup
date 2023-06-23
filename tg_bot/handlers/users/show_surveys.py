from aiogram import types
from aiogram.dispatcher.filters import Text
from loader import dp
from tg_bot.keyboards import inline_kb
from tg_bot.states.states import UserState, SurveyState
from tg_bot.utils.db_cruds import get_surveys, get_survey
from tg_bot.messages.messages import get_report_button_caption
from aiogram.dispatcher import FSMContext


@dp.callback_query_handler(Text('members'), state=[UserState, SurveyState, None])
async def show_surveys(cb: types.CallbackQuery):
    surveys= await get_surveys()
    if surveys:
        surveys_markup = types.InlineKeyboardMarkup(row_width=1)
        surveys_btn = []
        for survey in surveys:
            surveys_btn.append(types.InlineKeyboardButton(
                f'{survey["user"]}/ {survey["specialization"]}/ {survey["region"]}',
                callback_data=f'/{  survey["id"]}'))
        surveys_markup.add(*surveys_btn)
        await cb.message.answer(f'Для подробностей нажмите на анкету', reply_markup=surveys_markup)
        await UserState.survey.set()
    else:
        await cb.message.answer(
            'На данный момент анкет нет',
            reply_markup=inline_kb.base_menu
        )
    await cb.answer()


@dp.callback_query_handler(lambda callback_query: callback_query.data[0] == '/', state=UserState.survey)
async def manage_survey(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.edit_reply_markup()
    survey_id = int(callback_query.data[1:])
    survey = await get_survey(survey_id=survey_id)
    await callback_query.message.answer(
        f'Анкета которую Вы запросили:\nпользователь: {survey["user"]}\nимя: {survey["first_name"]}\nфамилия: {survey["last_name"]}\nдата рождения: {survey["birth_date"]}\n'
        f'специальность: {survey["specialization"]}\nстек: {survey["stack"]}\nхобби: {survey["hobby"]}\n'
        f'цель знакомства: {survey["acquaintance_goal"]}\nрегион: {survey["region"]}',
        reply_markup=inline_kb.base_menu)
    await state.finish()
    await callback_query.answer()
