from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from loader import dp
from tg_bot.keyboards import inline_kb

from datetime import date

from tg_bot.states.states import UserState, SurveyState
from tg_bot.utils.db_cruds import create_survey, create_user, get_survey


@dp.message_handler(Command('survey'), state=[UserState, SurveyState, None])
async def form(message: types.Message):
    username = message.from_user.username
    tg_id = message.from_user.id
    survey = await get_survey(username=username)
    if survey:
        await message.answer(
            f'Ваша анкета зарегистрирована:\nпользователь: {survey["user"]}\nимя: {survey["first_name"]}\nфамилия: {survey["last_name"]}\nдата рождения: {survey["birth_date"]}\n'
            f'специальность: {survey["specialization"]}\nстек: {survey["stack"]}\nхобби: {survey["hobby"]}\n'
            f'цель знакомства: {survey["acquaintance_goal"]}\nрегион: {survey["region"]}',
            reply_markup=inline_kb.base_menu)
    else:
        await message.answer(
            f'Введите Ваше имя:')
        await SurveyState.first_name.set()



@dp.message_handler(lambda msg: msg.text not in ['exit', '/start'], state=SurveyState.first_name)
async def specialization(message: types.Message, state: FSMContext):
    first_name = message.text
    await state.update_data(first_name=first_name)
    await message.answer('Введите Вашу фамилию:')
    await SurveyState.last_name .set()


@dp.message_handler(lambda msg: msg.text not in ['exit', '/start'], state=SurveyState.last_name )
async def specialization(message: types.Message, state: FSMContext):
    last_name = message.text
    await state.update_data(last_name=last_name)
    await message.answer('Введите Вашу специализацию:')
    await SurveyState.specialization.set()



@dp.message_handler(lambda msg: msg.text  not in ['exit', '/start'], state=SurveyState.specialization)
async def specialization(message: types.Message, state: FSMContext):
    specialization = message.text
    await state.update_data(specialization=specialization)
    await message.answer('Введите Ваш стэк:')
    await SurveyState.stack.set()


@dp.message_handler(lambda msg: msg.text not in ['exit', '/start'], state=SurveyState.stack)
async def stack(message: types.Message, state: FSMContext):
    stack = message.text
    await state.update_data(stack=stack)
    await message.answer('Введите Ваше хобби:')
    await SurveyState.hobby.set()


@dp.message_handler(lambda msg: msg.text  not in ['exit', '/start'], state=SurveyState.hobby)
async def hobby(message: types.Message, state: FSMContext):
    hobby = message.text
    await state.update_data(hobby=hobby)
    await message.answer('Введите цель знакомства')
    await SurveyState.goal.set()


@dp.message_handler(lambda msg: msg.text  not in ['exit', '/start'], state=SurveyState.goal)
async def goal(message: types.Message, state: FSMContext):
    acquaintance_goal = message.text
    await state.update_data(acquaintance_goal=acquaintance_goal)
    await message.answer('Введите Ваш регион:')
    await SurveyState.region.set()


@dp.message_handler(lambda msg: msg.text not in ['exit', '/start'], state=SurveyState.region)
async def region(message: types.Message, state: FSMContext):
    region = message.text
    await state.update_data(region=region)
    await message.answer('Введите дату рождения в формате "гггг-мм-дд')
    await SurveyState.birthdate.set()

@dp.message_handler(lambda msg: msg.text not in ['exit', '/start'], state=SurveyState.birthdate)
async def proceed_data_for_survey(message: types.Message, state: FSMContext):
    try:
        birth = date.fromisoformat(message.text)
        await state.update_data(birth_date=birth)
    except ValueError:
        await message.answer('Неверный ввод, побробуйте еще')
    username = message.from_user.username
    tg_id = message.from_user.id
    survey_data = await state.get_data()
    await create_user(username=username, tg_id=tg_id, first_name=survey_data['first_name'], last_name=survey_data['last_name'])
    await create_survey(username, **survey_data)
    survey = await get_survey(username=message.from_user.username)
    await message.answer(f'Ваша анкета зарегистрирована:\nпользователь: {survey["user"]}\nимя: {survey["first_name"]}\nфамилия: {survey["last_name"]}\nдата рождения: {survey["birth_date"]}\n'
            f'специальность: {survey["specialization"]}\nстек: {survey["stack"]}\nхобби: {survey["hobby"]}\n'
            f'цель знакомства: {survey["acquaintance_goal"]}\nрегион: {survey["region"]}', reply_markup=inline_kb.base_menu)
    await state.finish()


