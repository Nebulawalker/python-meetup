from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types.message import ContentTypes
from django.conf import settings

from loader import dp
from tg_bot.keyboards.inline_kb import get_donate_reply_markup
from tg_bot.states.states import DonateStates


@dp.message_handler(commands='donate', state='*')
async def handle_donate_command(message: types.Message):
    await handle_donate_start(message)


@dp.callback_query_handler(Text('donate'), state='*')
async def handle_donate_callback(callback_query: types.CallbackQuery):
    await handle_donate_start(callback_query.message)


async def handle_donate_start(message: types.Message):
    await DonateStates.amount_selection.set()
    await message.answer(
        text='Выберите сумму доната',
        reply_markup=get_donate_reply_markup())


@dp.callback_query_handler(state=DonateStates.amount_selection)
async def handle_amount_selection(
    callback_query: types.CallbackQuery,
    state: FSMContext,
):
    message = callback_query.message
    await message.delete()
    if callback_query.data == 'cancel_donate':
        await state.finish()
        await message.answer(
            'Оплата отменена',
            reply_markup=types.ReplyKeyboardRemove()
        )
        return

    async with state.proxy() as proxy_context:
        amount = int(callback_query.data)
        proxy_context['amount'] = amount
        prices = [
            types.LabeledPrice(label='Донат', amount=amount),
        ]
        await DonateStates.pre_checkout_query.set()
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
            is_flexible=False,
            prices=prices,
            start_parameter='python-meetup-donate',
            payload='HAPPY PYTHON MEETUP DONATE'
        )


@dp.pre_checkout_query_handler(
    lambda query: True,
    state=DonateStates.pre_checkout_query
)
async def checkout(
    pre_checkout_query: types.PreCheckoutQuery,
    state: FSMContext
):
    await pre_checkout_query.bot.answer_pre_checkout_query(
        pre_checkout_query.id,
        ok=True,
        error_message="Ошибка! Повторите попытку платежа позже"
    )
    await DonateStates.successful_payment.set()


@dp.message_handler(
    content_types=ContentTypes.SUCCESSFUL_PAYMENT,
    state=DonateStates.successful_payment,
)
async def got_payment(message: types.Message, state: FSMContext):
    message_text = (
        'Прошла оплата за донат'
        f' `{message.successful_payment.total_amount / 100}'
        f' {message.successful_payment.currency}`'
        ' Спасибо!'
        '\n\nИспользуйте /donate чтобы отправить еще'
    )
    await message.answer(
        text=message_text,
        parse_mode='Markdown'
    )
    await state.finish()
