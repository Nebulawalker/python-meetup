from aiogram import types

base_menu = types.InlineKeyboardMarkup(row_width=3)
base_menu_buttons = [
    types.InlineKeyboardButton('Начать', callback_data='start'),
    types.InlineKeyboardButton('Анкеты', callback_data='members'),
    types.InlineKeyboardButton('Доклады', callback_data='reports'),
]
base_menu.add(*base_menu_buttons)

question_menu = types.InlineKeyboardMarkup(row_width=1)
question_menu_buttons = [
    types.InlineKeyboardButton('Задать вопрос', callback_data='question'),
]
question_menu.add(*question_menu_buttons)


answer_menu = types.InlineKeyboardMarkup(row_width=1)
answer_menu_buttons = [
    types.InlineKeyboardButton('Ответить на вопрос', callback_data='answer'),
]
answer_menu.add(*answer_menu_buttons)


def get_donate_reply_markup():
    reply_markup = types.InlineKeyboardMarkup(row_width=2)
    buttons = [
        types.InlineKeyboardButton('500 руб.', callback_data='50000'),
        types.InlineKeyboardButton('1000 руб.', callback_data='100000'),
        types.InlineKeyboardButton('Другая', callback_data='other_amount'),
        types.InlineKeyboardButton('Отмена', callback_data='cancel_donate'),
    ]
    reply_markup.add(*buttons)

    return reply_markup
