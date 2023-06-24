from aiogram import types
from aiogram.dispatcher.filters import Text
from loader import dp
from aiogram.dispatcher import FSMContext
from tg_bot.states.states import UserState, MessageState
from tg_bot.keyboards import inline_kb
from tg_bot.messages.messages import ABOUT_MSG
from tg_bot.utils.db_cruds import is_user_reporter


@dp.message_handler(commands='about')
async def intro(message: types.Message):
    await message.answer(
        ABOUT_MSG, reply_markup=inline_kb.base_menu
    )


@dp.message_handler(commands='start', state='*')
async def start_conversation(message: types.Message, state: FSMContext):
    reporter = await is_user_reporter(message.from_user.id)
    if not reporter:
        await message.answer(
            f'Здравствуйте {message.from_user.username}! Приветствуем Вас на мероприятии python-meetup!\n'
            f'Я - Бот-помощник! Могу предоставить информации о нашем мероприятии, помогу задать вопросы спикерам, '
            f'познакомить с другими участниками!\n'
            f'Что-бы узнать больше нажмите кнопку /help в меню.',
            reply_markup=inline_kb.base_menu
        )
        # await message.answer(
        #     'Сделайте выбор',
        #     reply_markup=inline_kb.hearer_main_menu
        # )
    else:
        await message.answer(
            f'Здравствуйте {message.from_user.username}! Приветствуем Вас на мероприятии python-meetup!\n'
            f'Я - Бот-помощник! Могу предоставить информации о нашем мероприятии, помогу задать вопросы спикерам, '
            f'познакомить с другими участниками!\n'
            f'Что-бы узнать больше нажмите кнопку /help в меню.',
            reply_markup=inline_kb.base_menu
        )
        await message.answer('Вы заявлены как спикер по следующим докладам # Далее список докладов')
        # await message.answer(
        #     'Сделайте выбор',
        #     reply_markup=inline_kb.reporter_main_menu
        # )
    await state.finish()


@dp.callback_query_handler(Text('start'), state='*')
async def button_start(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.edit_reply_markup()
    reporter = await is_user_reporter(callback_query.message.from_user.id)
    if not reporter:
        await callback_query.message.answer(
            f'Здравствуйте {callback_query.from_user.username}! Приветствуем Вас на мероприятии python-meetup!\n'
            f'Я - Бот-помощник! Могу предоставить информации о нашем мероприятии, помогу задать вопросы спикерам, '
            f'познакомить с другими участниками!\n'
            f'Что-бы узнать больше нажмите кнопку /help в меню.',
            reply_markup=inline_kb.base_menu
            )
        # await message.answer(
        #     'Сделайте выбор',
        #     reply_markup=inline_kb.hearer_main_menu
        # )
    else:
        await callback_query.message.answer(f'Здравствуйте {callback_query.from_user.username}! Приветствуем Вас на '
                                            f'мероприятии python-meetup!\nЯ - Бот-помощник! Могу предоставить '
                                            f'информации о нашем мероприятии, помогу задать вопросы спикерам, '
                                            f'познакомить с другими участниками!\nЧто-бы узнать больше нажмите кнопку '
                                            f'/help в меню.',
                                            reply_markup=inline_kb.base_menu
                                            )
        await callback_query.message.answer('Вы заявлены как спикер по следующим докладам # Далее список докладов')
        # await message.answer(
        #     'Сделайте выбор',
        #     reply_markup=inline_kb.reporter_main_menu
        # )
    await state.finish()


@dp.message_handler(lambda msg: msg.text[0] != '/' and msg.text != 'exit',
                    state=[UserState, MessageState.standby, None])
async def start_conversation(message: types.Message, state: FSMContext):
    await message.answer('Сделайте выбор', reply_markup=inline_kb.base_menu)
    await state.finish()
