from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from loader import dp

from datetime import date

from tg_bot.states.states import UserState, SurveyState
from tg_bot.utils.db_cruds import create_survey, create_user


@dp.callback_query_handler(Text('form'), state=[UserState, SurveyState, None])
async def form(callback_query: types.CallbackQuery):
    username = callback_query.from_user.username
    tg_id = callback_query.from_user.id
    await create_user(username, tg_id)
    await callback_query.message.answer(
        f'Введите дату рождения в формате "гггг-мм-дд":'
    )
    await SurveyState.birthdate.set()
    await callback_query.answer()


@dp.message_handler(state=SurveyState.birthdate)
async def birthdate(message: types.Message, state: FSMContext):
    birth = date.fromisoformat(message.text)
    await state.update_data(birth_date=birth)
    await message.answer('Введите Вашу специализацию:')
    await SurveyState.specialization.set()


@dp.message_handler(state=SurveyState.specialization)
async def specialization(message: types.Message, state: FSMContext):
    specialization = message.text
    await state.update_data(specialization=specialization)
    await message.answer('Введите Ваш стэк:')
    await SurveyState.stack.set()


@dp.message_handler(state=SurveyState.stack)
async def stack(message: types.Message, state: FSMContext):
    stack = message.text
    await state.update_data(stack=stack)
    await message.answer('Введите Ваше хобби:')
    await SurveyState.hobby.set()


@dp.message_handler(state=SurveyState.hobby)
async def hobby(message: types.Message, state: FSMContext):
    hobby = message.text
    await state.update_data(hobby=hobby)
    await message.answer('Введите цель знакомства')
    await SurveyState.goal.set()


@dp.message_handler(state=SurveyState.goal)
async def goal(message: types.Message, state: FSMContext):
    acquaintance_goal = message.text
    await state.update_data(acquaintance_goal=acquaintance_goal)
    await message.answer('Введите Ваш регион:')
    await SurveyState.region.set()


@dp.message_handler(state=SurveyState.region)
async def proceed_data_for_survey(message: types.Message, state: FSMContext):
    region = message.text
    username = message.from_user.username
    await state.update_data(region=region)
    survey_data = await state.get_data()
    print(survey_data)
    print(username)
    await create_survey(username, **survey_data)
    await message.answer('Good')
    await state.finish()