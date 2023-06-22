import os
import django
from datetime import date

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "python_meetup.settings")
django.setup()
from django.conf import settings
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import funcs
import markups as m
from asgiref.sync import sync_to_async

bot = Bot(settings.TELEGRAM_BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


class UserState(StatesGroup):
    report = State()


class SurveyState(StatesGroup):
    birthdate = State()
    spec = State()
    stack = State()
    hobby = State()
    goal = State()
    region = State()


@dp.message_handler(text='exit', state=[UserState, SurveyState, None])
async def exit_proceed(msg: types.Message, state: FSMContext):
    await msg.answer('Всего доброго, берегите себя')
    await state.finish()


@dp.message_handler(state=[not SurveyState, UserState, None])
async def start_conversation(msg: types.Message):
    status = await sync_to_async(funcs.identify_user)(msg.from_user.id)
    if status == 'hearer':
        await msg.answer(
            f'Здравствуйте {status}: {msg.from_user.username} для выхода в любом месте наберите "exit", '
            f'для подробного ознакомления с функциональностью чата нажмите кнопку "О нас"',
            reply_markup=m.base_menu)
        await msg.answer('Сделайте выбор', reply_markup=m.hearer_main_menu)
    else:
        await msg.answer(f'Здравствуйте  {status}: {msg.from_user.username} для выхода в любом месте наберите "exit",',
                         reply_markup=m.base_menu)
        await msg.answer('Сделайте выбор', reply_markup=m.reporter_main_menu)


@dp.callback_query_handler(Text('reports'), state=[UserState, SurveyState, None])
async def intro(cb: types.CallbackQuery):
    reports = await sync_to_async(funcs.get_reports)()
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


@dp.callback_query_handler(lambda cb: cb.data[0] == '/', state=UserState.report)
async def manage_report(cb: types.CallbackQuery, state: FSMContext):
    report_id = int(cb.data[1:])
    report = await sync_to_async(funcs.get_report)(report_id)
    if report['is_current']:
        await cb.message.answer(f'Доклад сейчас идёт\nТема: {report["topic"]},\nДокладчик: {report["speaker"]},\n'
                                f'Начало: {report["starts_at"]},\nКонец: {report["ends_at"]}', reply_markup=m.base_menu)
    else:
        await cb.message.answer(
            f'Тема: {report["topic"]},\nДокладчик: {report["speaker"]},\nНачало: {report["starts_at"]},'
            f'\nКонец: {report["ends_at"]}', reply_markup=m.base_menu)
    await state.finish()
    await cb.answer()


# hearer block start====================================================================================================
@dp.callback_query_handler(Text('intro'), state=[UserState, SurveyState, None])
async def intro(cb: types.CallbackQuery):
    await bot.send_document(chat_id=cb.from_user.id, document=open('intro'),
                            reply_markup=m.hearer_main_menu)
    await cb.answer()


@dp.callback_query_handler(Text('form'), state=[UserState, SurveyState, None])
async def form(cb: types.CallbackQuery):
    username = cb.from_user.username
    tg_id = cb.from_user.id
    await sync_to_async(funcs.create_user)(username, tg_id)
    await cb.message.answer(f'введите дату рождения в формате "гггг-мм-дд"')
    await SurveyState.birthdate.set()
    await cb.answer()


@dp.message_handler(state=SurveyState.birthdate)
async def birthdate(msg: types.Message, state: FSMContext):
    birth = date.fromisoformat(msg.text)
    await state.update_data(birth_date=birth)
    await msg.answer('введите Вашу специализацию')
    await SurveyState.spec.set()


@dp.message_handler(state=SurveyState.spec)
async def specialization(msg: types.Message, state: FSMContext):
    specialization = msg.text
    await state.update_data(specialization=specialization)
    await msg.answer('введите Ваш стэк')
    await SurveyState.stack.set()


@dp.message_handler(state=SurveyState.stack)
async def stack(msg: types.Message, state: FSMContext):
    stack = msg.text
    await state.update_data(stack=stack)
    await msg.answer('введите Ваше хобби')
    await SurveyState.hobby.set()


@dp.message_handler(state=SurveyState.hobby)
async def hobby(msg: types.Message, state: FSMContext):
    hobby = msg.text
    await state.update_data(hobby=hobby)
    await msg.answer('введите цель знакомства')
    await SurveyState.goal.set()


@dp.message_handler(state=SurveyState.goal)
async def goal(msg: types.Message, state: FSMContext):
    acquaintance_goal = msg.text
    await state.update_data(acquaintance_goal=acquaintance_goal)
    await msg.answer('введите Ваш регион')
    await SurveyState.region.set()


@dp.message_handler(state=SurveyState.region)
async def proceed_data_for_survey(msg: types.Message, state: FSMContext):
    region = msg.text
    username = msg.from_user.username
    await state.update_data(region=region)
    survey_data = await state.get_data()
    print(survey_data)
    print(username)
    await sync_to_async(funcs.create_survey)(username, **survey_data)
    await msg.answer('Good')
    await state.finish()


# hearer block start====================================================================================================

executor.start_polling(dp)
