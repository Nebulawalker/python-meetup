import os
import django

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


@dp.message_handler(text='exit', state=[UserState, None])
async def exit_proceed(msg: types.Message, state: FSMContext):
    await msg.answer('Всего доброго, берегите себя')
    await state.finish()


@dp.message_handler(state=[UserState, None])
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


@dp.callback_query_handler(Text('reports'), state=[UserState, None])
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
@dp.callback_query_handler(Text('intro'), state=[UserState, None])
async def intro(cb: types.CallbackQuery):
    await bot.send_document(chat_id=cb.from_user.id, document=open('intro'),
                            reply_markup=m.hearer_main_menu)
    await cb.answer()


# hearer block start====================================================================================================

executor.start_polling(dp)
