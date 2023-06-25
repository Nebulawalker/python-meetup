from aiogram import types
from aiogram.dispatcher.filters import Text
from loader import dp
from tg_bot.keyboards import inline_kb
from tg_bot.states.states import MessageState
from tg_bot.utils.db_cruds import send_message, is_user, send_answer
from aiogram.dispatcher import FSMContext
from loader import bot

issue_identification = {}


@dp.callback_query_handler(Text('question'), state='*')
async def question(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.edit_reply_markup()
    being_user = await is_user(callback_query.from_user.id)
    if being_user:
        await callback_query.message.answer('Задайте вопрос')
        data = await state.get_data()
        report_id = data['report_id']
        print(report_id)
        await MessageState.question.set()
    else:
        await callback_query.message.answer('Вначале заполните анкету')
        await state.finish()


@dp.message_handler(lambda msg: msg.text not in ['exit', '/start'], state=MessageState.question)
async def proceed_question(message: types.Message, state: FSMContext):
    from_whom_username = message.from_user.username
    data = await state.get_data()
    report_id = data['report_id']
    details_issue = await send_message(message=message.text, from_whom_username=from_whom_username, report_id=report_id)
    chat_id, issue_id = details_issue
    message = ''.join((f'Вопрос от {from_whom_username}:\n', message.text))
    issue_identification[f'{from_whom_username}'] = issue_id
    print(issue_identification)
    await bot.send_message(chat_id, message, reply_markup=inline_kb.answer_menu)
    await state.finish()


@dp.callback_query_handler(Text('answer'), state='*')
async def answer(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.edit_reply_markup()
    username = callback_query.message.text.split(':')[0].split()[-1]
    await state.update_data(username=username)
    await callback_query.message.answer('Ответьте на вопрос')
    await MessageState.answer.set()


@dp.message_handler(lambda msg: msg.text not in ['exit', '/start'], state=MessageState.answer)
async def proceed_answer(message: types.Message, state: FSMContext):
    data = await state.get_data()
    username = data['username']
    issue_id = issue_identification[f'{username}']
    print(issue_id)
    chat_id = await send_answer(message=message.text, issue_id=issue_id)
    print('chat id:=====', chat_id)
    await bot.send_message(chat_id, message.text)
    await message.answer('Благодарим за ответ')
    await state.finish()
