from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from django.conf import settings

from loader import dp
from tg_bot.states.states import DonateStates


@dp.callback_query_handler(state=DonateStates.amount_selection)
async def handle_amount_selection(
    callback_query: types.CallbackQuery,
    state: FSMContext,
):
    message = callback_query.message
    if callback_query.data == 'cancel_donate':
        await state.finish()
        await message.delete()
        await message.answer(
            'Оплата отменена',
            reply_markup=types.ReplyKeyboardRemove()
        )

    async with state.proxy() as proxy_context:
        amount = int(callback_query.data)
        proxy_context['amount'] = amount
        prices = [
            types.LabeledPrice(label='Донат', amount=amount),
        ]
        await callback_query.bot.send_invoice(
            message.chat.id,
            title='Донат в пользу "Python meetup"',
            description='Решили помочь с проведением митапов по Python? '
            'Оплатите донат!',
            provider_token=settings.PAYMENTS_PROVIDER_TOKEN,
            currency='rub',
            photo_url=settings.INVOICE_IMAGE_URL,
            photo_height=201,
            photo_width=251,
            photo_size=512,
            prices=prices,
            start_parameter='python-meetup-donate',
            payload='HAPPY PYTHON MEETUP DONATE'
        )


async def handle_donate_start(message: types.Message):
    reply_markup = types.InlineKeyboardMarkup(row_width=2)
    buttons = [
        types.InlineKeyboardButton('500 руб.', callback_data='50000'),
        types.InlineKeyboardButton('1000 руб.', callback_data='100000'),
        types.InlineKeyboardButton('Другая', callback_data='other_amount'),
        types.InlineKeyboardButton('Отмена', callback_data='cancel_donate'),
    ]
    await DonateStates.amount_selection.set()
    reply_markup.add(*buttons)
    await message.answer('Выберите сумму доната', reply_markup=reply_markup)


@dp.message_handler(commands='donate')
async def handle_donate_command(message: types.Message):
    await handle_donate_start(message)


@dp.callback_query_handler(Text('donate'))
async def handle_donate_callback(callback_query: types.CallbackQuery):
    await handle_donate_start(callback_query.message)
